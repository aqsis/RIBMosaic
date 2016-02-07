# #############################################################################
# AUTHOR BLOCK:
# #############################################################################
#
# RIB Mosaic RenderMan(R) IDE, see <http://sourceforge.net/projects/ribmosaic>
# by Eric Nathen Back aka WHiTeRaBBiT, 01-24-2010
# This script is protected by the GPL: Gnu Public License
# GPL - http://www.gnu.org/copyleft/gpl.html
#
# #############################################################################
# GPL LICENSE BLOCK:
# #############################################################################
#
# Script Copyright (C) Eric Nathen Back
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# #############################################################################
# COPYRIGHT BLOCK:
# #############################################################################
#
# The RenderMan(R) Interface Procedures and Protocol are:
# Copyright 1988, 1989, 2000, 2005 Pixar
# All Rights Reserved
# RenderMan(R) is a registered trademark of Pixar
#
# #############################################################################
# COMMENT BLOCK:
# #############################################################################
#
# RIB export module to translate and write Blender geometry data to
# RIB archives, can also be compiled into Python C module using Cython.
#
# This script is PEP 8 compliant
#
# Search TODO for incomplete code
# Search FIXME for improper code
# Search XXX for broken code
#
# #############################################################################
# END BLOCKS
# #############################################################################

import bpy
import math
import os
import mathutils
import string


# #### Global variables

#MODULE = os.path.dirname(__file__).split(os.sep)[-1]
#exec("import " + MODULE + " as rm")

DEBUG_PRINT = True




# #############################################################################
# GEOMETRY EXPORT CLASS
# #############################################################################

# ##### Define the ribify class for script export of RIB primitives
class Ribify():
    """The ribify class provides all methods required to export geometry data
    of all types from Blender to RenderMan.
    """

    # ### Public attributes

    pointer_file = None  # File object to write RIB to
    is_gzip = False  # If file gzipped
    indent = 0  # how many tabs to indent from the left
    vertcount = 0 # highest vertex index used by faces
    materials_used = [] # list of material indexes used by faces

    # vars for tracking array items output
    itemcount = 0  # number of array items that have been outputed
    items_per_line = 3  # number of array items per line


    def _start_rib_array(self, items_per_line=3, indent=True):
        self.itemcount = 0
        self.firstline = True
        self.items_per_line = items_per_line
        self.write_text('[', indent)


    def _write_rib_array_item(self, item, debug=False):

        # if on the first item of the line then indent
        if self.itemcount == 0:
            self.write_text('\n', False)
        else:
            # adding another item on the line so just put a space
            #  between items don't use indentation
            self.write_text(' ', False)
        # output the item in the list, indent if first item
        if(debug):
          print("write: ",item, "file:" , type(self.pointer_file))
        self.write_text(str(item), self.itemcount == 0)
        self.itemcount += 1

        # only allow so many items per line
        if self.itemcount == self.items_per_line:
            self.itemcount = 0

    def _end_rib_array(self):
        # end of the RIB array list block
        self.write_text('\n', False)
        self.write_text(']\n')

    def _write_rib_array_list(self, vect, debug=False):
        for v in vect:
            self._write_rib_array_item(v,debug)

    def _export_faces(self, mesh):
        self.vertcount = 0
        self.materials_used = []
        self.inc_indent()
        # output the number of vertices for each face
        self._start_rib_array(1)
        for p in mesh.polygons:
            self._write_rib_array_item(p.loop_total)

            # Populate materials_used list with faces material indexes
            if (not p.material_index in self.materials_used):
                self.materials_used.append(p.material_index)
            
        self._end_rib_array()

        # output the vertex index for each face corner
        # all vertex indices per face need to be on one line 
        # --> due to submesh cache ( ExportMeshdata._ribify_cache )
        
        self._start_rib_array(1)
        for p in mesh.polygons:
            # keep track of the highest vertex index used
            self.vertcount = max(self.vertcount,max(p.vertices))
            self._write_rib_array_item(" ".join([str(v) for v in p.vertices]))
        self._end_rib_array()

    def _export_creases(self, mesh):
        # export blender mesh edges that have a crease value != 0
        Creases = [e for e in mesh.edges if e.crease != 0]
        self._start_rib_array(5)
        self._write_rib_array_item('"interpolateboundary"')
        for edge in Creases:
            self._write_rib_array_item('"crease"')
        self._end_rib_array()

        self._start_rib_array(1)
        self._write_rib_array_item("0 0")
        # write out data arrangement for creases:
        # first array set has 2 values for each crease
        # second array set has 1 value for each crease
        for edge in Creases:
            self._write_rib_array_item("2 1")
        self._end_rib_array()

        # output first array set:
        # use two vertex indices to define each crease
        self._start_rib_array(1)
        for edge in Creases:
            self._write_rib_array_item('%i %i' % (edge.vertices[0], edge.vertices[1]))
        self._end_rib_array()

        # output second array set which is the crease sharpness weight value
        self._start_rib_array(1)
        for edge in Creases:
            #Calculate crease up to 5.5
            #(looks the same as blenders up to that point)
            crease = edge.crease * 5.5
            #After 5.0 increase sharpening rate to match blenders rate
            if (crease > 5.0): crease = crease + ((crease - 5.0) * 6)
            self._write_rib_array_item(crease)

        self._end_rib_array()

    def _export_vertices(self, mesh):

        # rare that these conditions occur but check to make sure
        # there are faces and vertices to export
        if len(mesh.vertices) == 0:
            return

        self.write_text('"P"\n')
        self._start_rib_array(3)
        for i in range(0, self.vertcount + 1):
            self._write_rib_array_list(mesh.vertices[i].co)
        self._end_rib_array()


    def _export_normals(self, primvar_rib, mesh, per_vertex=True):
        # rare that these conditions occur but check to make sure
        # there are faces and vertices to export
        if len(mesh.vertices) == 0 or len(mesh.polygons) == 0:
            return

        self.write_text(primvar_rib)
        if per_vertex:
            self._start_rib_array(3)
            for i in range(0, self.vertcount + 1):
                self._write_rib_array_list(mesh.vertices[i].normal)
        else:
            self._start_rib_array(1)
            for p in mesh.polygons:
                # iterate through each vertex index in the face
                norm_str = ""
                for vi in p.vertices:
                    # build the normals list
                    # if face is smooth then use the vertex normal
                    if p.use_smooth:
                        norm_str += " ".join([str(c) for c in mesh.vertices[vi].normal])
                    else:
                        # otherwise the face is flat so use the face normal
                        norm_str += " ".join([str(c) for c in p.normal])
                    norm_str += " "
                self._write_rib_array_item(norm_str)
        self._end_rib_array()


    def _export_uvs(self, primvar_rib, mesh, name=""):

        uvs = []
        
        # uv_loop_layer is of type MeshUVLoopLayer
        
        if name == "":
            uv_loop_layer = mesh.uv_layers.active  
        else:
            # assuming uv loop layers and uv textures share identical indices
            idx = mesh.uv_textures.keys().index(name)
            uv_loop_layer = mesh.uv_layers[idx] 

        if uv_loop_layer is None:
            return None
        
        # get all uvs for each polygon
        for poly in mesh.polygons:
            poly_uvs = []
            for loop_index in poly.loop_indices:
                poly_uvs.append(       uv_loop_layer.data[loop_index].uv.x )
                poly_uvs.append( 1.0 - uv_loop_layer.data[loop_index].uv.y )
                ## renderman expects UVs flipped vertically from blender
            uvs.append(poly_uvs)  
        
        print("Creating: uvs, poly count:",len(uvs), uvs)
        
        # write rib
        self.write_text(primvar_rib)
        self._start_rib_array(1)
        # all uv data for a face must be on one line
        for polyuv in uvs:
            polyuv_str = " ".join([str(v) for v in polyuv]) #     8 values "x y x y x y x y" for quad polygons
            self._write_rib_array_item(polyuv_str)
        
        self._end_rib_array()

    # ### Public methods

    def write_text(self, text="", use_indent=True):
        """Writes text to open file handle. Also properly writes text as either
        encoded binary or text mode according to is_gzip bool. This method also
        exists in the  ExporterArchive class but is duplicated here to simplify
        file management in the Ribify C++ module.

        text = The text to write (can contain escape characters)
        """

        if text:
            if self.pointer_file:
                if use_indent and self.indent > 0:
                    text = " ".rjust(self.indent * 4) + text
                if self.is_gzip:
                    self.pointer_file.write(text.encode())
                else:
                    self.pointer_file.write(text)
            else:
                raise RibmosaicError("Archive already closed,"
                                     "cannot write text")

    def inc_indent(self):
        self.indent += 1

    def dec_indent(self):
        self.indent -= 1
        if self.indent < 0:
            self.indent = 0


    def data_to_primvar(self,  datablock, **primvar):
        """Append to file_object specified data-block member from Blender
        data-block into RenderMan primitive variable as class type using
        specified define name.

        datablock = Blender mesh data
        **primvar = dictionary containing following members:
        member = data-block member to build primvar from (such as Normal, ect)
        define = what will the primvar be called
        ptype = primitive data type
        pclass = primitive class to order quantities by
        """
        if DEBUG_PRINT:
            print("Creating", primvar['define'], "as", primvar['ptype'],
                  "sorted as", primvar['pclass'], "for", primvar['member'],
                  "in", datablock, "...")

        member = primvar['member']
        primvar_rib = '"%s %s %s"\n' % (primvar['pclass'], primvar['ptype'], primvar['define'])
        # figure out what mesh data to output for primvar
        if member == 'N':
            # determine if per vertex normals wanted instead of face
            per_vertex = primvar['pclass'][0:4] != 'face'
            self._export_normals(primvar_rib, datablock, per_vertex)
        elif member == 'UV':
            self._export_uvs(primvar_rib, datablock)



    def mesh_pointspolygons(self, datablock):
        """ """
        if DEBUG_PRINT:
            print("Creating pointpolygons...")

        self.write_text('PointsPolygons \n')
        self.inc_indent()
        self._export_faces(datablock)
        self._export_vertices(datablock)


    def mesh_subdivisionmesh(self, datablock):
        """ """
        if DEBUG_PRINT:
            print("Creating subdivisionmesh...")

        self.write_text('SubdivisionMesh "catmull-clark"\n')
        self.inc_indent()
        self._export_faces(datablock)

        # if there are creases then need to write crease info
        self._export_creases(datablock)

        # output vertices
        self._export_vertices(datablock)


    def mesh_points(self, datablock):
        """ """
        if DEBUG_PRINT:
            print("Creating mesh points...")

        self.write_text('Points\n')
        self.inc_indent()
        # output vertices
        self.vertcount = len(datablock.vertices) - 1
        self._export_vertices(datablock)

    def mesh_curves(self, datablock):
        """ """

        print("Creating mesh curves...")

    def particles_points(self, datablock):
        """ """

        print("Creating particle points...")

    def particles_curves(self, datablock):
        """ """

        print("Creating particle curves...")

    def curve_cyclic_poly(self, datablock):
        """ """

        print("Creating cyclic poly curves...")

    def curve_cyclic_bezier(self, datablock):
        """ """

        print("Creating cyclic bezier curves...")

    def curve_cyclic_nurbs(self, datablock):
        """ """

        print("Creating cyclic nurbs curves...")

    def curve_noncyclic_poly(self, datablock):
        """ """

        print("Creating noncyclic poly curves...")

    def curve_noncyclic_bezier(self, datablock):
        """ """

        print("Creating noncyclic bezier curves...")

    def curve_noncyclic_nurbs(self, datablock):
        """ """

        print("Creating noncyclic nurbs curves...")

    def curve_points(self, datablock):
        """ """

        print("Creating curve points...")

    def surface_nupatch(self, datablock):
        """ """

        print("Creating nupatch...")

    def surface_points(self, datablock):
        """ """

        print("Creating surface points...")

    def metaball_blobby(self, datablock):
        """ """

        print("Creating meta blobby...")

    def metaball_points(self, datablock):
        """ """

        print("Creating meta points...")

    def matrix4x4(self, mat):
        """ Export a blender 4x4 matrix in RIB format"""
        self.inc_indent()
        self.inc_indent()
        self._start_rib_array(4, False)
        for i in range(4):
            for j in range(4):
                self._write_rib_array_item(mat[j][i])
        self._end_rib_array()
        self.write_text('\n')
