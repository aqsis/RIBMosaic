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
# RIB export module to translate and write Blender geometry data to RIB archives,
# can also be compiled into Python C module using Cython.
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




# #############################################################################
# GEOMETRY EXPORT CLASS
# #############################################################################

# ##### Define the ribify class for script export of RIB primitives

class Ribify():
    """The ribify class provides all methods required to export geometry data
    of all types from Blender to RenderMan.
    """
    
    
    # ### Public attributes
    
    pointer_file = None # File object to write RIB to
    is_gzip = False # If file gzipped
    
    
    # ### Public methods
    
    def write_text(self, text=""):
        """Writes text to open file handle. Also properly writes text as either
        encoded binary or text mode according to is_gzip bool. This method also
        exists in the  ExporterArchive class but is duplicated here to simplify
        file management in the Ribify C++ module.
        
        text = The text to write (can contain escape characters)
        """
        
        if text:
            if self.pointer_file:
                if self.is_gzip:
                    self.pointer_file.write(text.encode())
                else:
                    self.pointer_file.write(text)
            else:
                raise RibmosaicError("Archive already closed, cannot write text")
    
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
        
        print("Creating", primvar['define'], "as", primvar['ptype'], "sorted as",
              primvar['pclass'], "for", primvar['member'], "in", datablock, "...")
    
    def mesh_pointspolygons(self, datablock):
        """ """
        
        print("Creating pointpolygons...")
    
    def mesh_subdivisionmesh(self, datablock):
        """ """
        
        print("Creating subdivisionmesh...")
    
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



