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

MODULE = os.path.dirname(__file__).split(os.sep)[-1]
exec("import " + MODULE + " as rm")

DEBUG_PRINT = False




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

    # decomposed data from a blender mesh
    nverts = []  # list of vertex count for each face
    verts = []  # list of vertex indices for each face
    P = []  # list of vertex points
    uvs = []
    N = []  # list of normals for each face
    vertcount = 0 # highest vertex index used by faces

    # local helper functions
    # Mesh data access
    def _decompose_mesh(self, mesh):
        # clear all of the lists
        self.nverts = []
        self.verts = []
        self.P = []
        self.uvs = []
        self.N = []
        self.vertcount = 0

        for f in mesh.faces:
            n = len(f.vertices)
            # add the number of vertices to the nverts list
            self.nverts += [n]
            # iterate through each vertex index in the face
            for a in range(0, n):
                #get the index of the vertice
                vi = f.vertices[a]
                # keep track of the highest vertex index used
                if vi > self.vertcount:
                    self.vertcount = vi
                # add the index to the verts list of indices
                self.verts += [vi]
                # build the normals list
                # if face is smooth then use the mesh.vertices[index].normal
                if f.use_smooth:
                    v = mesh.vertices[vi]
                    self.N += [v.normal[0], v.normal[1], v.normal[2]]
                else:
                    # otherwise the face is flat so use the face normal
                    self.N += [f.normal[0], f.normal[1], f.normal[2]]

        # only build a list of verts used by the faces
        for i in range(0, self.vertcount + 1):
            co = mesh.vertices[i].co
            self.P += [co[0], co[1], co[2]]

        try:
            #FIXME should be exporting all the uv layers not just the active
            uv_layer = mesh.uv_textures.active.data
        except:
            uv_layer = None

        if uv_layer:
            f_uvs = {}  # sequence array of uv for each face
            for fi, tf in enumerate(uv_layer):
                # "1.0 -" because
                # renderman expects UVs flipped
                # vertically from blender

                f_uvs[fi] = [tf.uv1[0], 1.0 - tf.uv1[1]]
                f_uvs[fi] += [tf.uv2[0], 1.0 - tf.uv2[1]]
                f_uvs[fi] += [tf.uv3[0], 1.0 - tf.uv3[1]]
                if len(mesh.faces[fi].vertices) == 4:
                    f_uvs[fi] += [tf.uv4[0], 1.0 - tf.uv4[1]]

            for uv in f_uvs.values():
                self.uvs.extend(uv)
        else:
            self.uvs = None


    def _export_faces(self):
        self.inc_indent()
        self.write_rib_list(self.nverts, 10, 12)
        self.write_rib_list(self.verts, 3, 12)
        self.write_text('\n')

    def _export_vertices(self):
        self.write_text('"P"\n')
        self.write_rib_list(self.P, 3, 14)

    def _export_normals(self):
        # TODO eventually this should be done by data_to_primvar()
        if self.N:
            self.write_text('\n')
            self.write_text('"facevarying normal N"\n')
            self.write_rib_list(self.N, 3, 14)

    def _export_uvs(self):
        # TODO eventually this should be done by data_to_primvar()
        if self.uvs:
            self.write_text('\n')
            self.write_text('"facevarying float[2] st"\n')
            self.write_rib_list(self.uvs, 2, 14)

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

    def write_rib_list(self, list, items_per_line=3, space_indent=1):
        itemcount = 0
        firstline = True
        self.write_text('[')

        for i in list:
            # if on the first item of the line then indent
            if itemcount == 0 and not firstline:
                self.write_text('\n', False)
                self.write_text('  ')
            else:
                # adding another item on the line so just put a space
                #  between items don't use indentation
                self.write_text(' ', False)
            # output the item in the list but with no indentation
            self.write_text(str(i), False)
            itemcount += 1

            # only allow so many items per line
            if itemcount == items_per_line:
                itemcount = 0
                firstline = False

        # end of the RIB array list block
        self.write_text(' ]\n', False)

    def data_to_primvar(self, datablock, **primvar):
        """Append to file_object specified data-block member from Blender
        data-block into RenderMan primitive variable as class type using
        specified define name.

        datablock = Blender mesh data-block
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

    def mesh_pointspolygons(self, datablock, smooth_normals=False):
        """ """

        if DEBUG_PRINT:
            print("Creating pointpolygons...")

        self._decompose_mesh(datablock)


        self.write_text('PointsPolygons \n')
        self.inc_indent()
        self._export_faces()
        self._export_vertices()

        # FIXME should be based on user options
        # for now its just for testing
        self._export_uvs()
        # FIXME should be based on user options
        # for now its just for testing
        self._export_normals()

    def mesh_subdivisionmesh(self, datablock):
        """ """
        if DEBUG_PRINT:
            print("Creating subdivisionmesh...")
        self._decompose_mesh(datablock)

        self.write_text('SubdivisionMesh "catmull-clark"\n')
        self._export_faces()

        # if there are creases then need to write crease info
        self.write_text('["interpolateboundary"] [0 0] [] []\n')

        # output vertices
        self._export_vertices()

        # FIXME should be based on user options
        # for now its just for testing
        self._export_uvs()
        # FIXME should be based on user options
        # for now its just for testing
        self._export_normals()

    def mesh_points(self, datablock):
        """ """

        print("Creating mesh points...")

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
