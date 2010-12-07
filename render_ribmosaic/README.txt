Welcome to RIB Mosaic!

REQUIREMENTS:
- Blender 2.5x series
- Python 3.x (the version bundled with Blender should work fine)
- RenderMan compliant renderer

INSTALLATION:
Download and install Blender and your favorite RenderMan compliant renderer.
The installation of this add-on depends on how you recieved it...

- If you received this in a zipped add-on archive then start Blender, go to
  "File->User Preferences...->Add-Ons->Install Add-On...". Browse to and double
  click on the zip file to install (you may need to disable filtering).

- If you received this from a source repository, then copy this folder to Blender's
  "BLENDERHOME/2.5*/scripts/addons" folder to install.

Once installed start Blender and go to "File->User Preferences->Add-Ons" and
enable the RIB Mosaic add-on check box to the right.

STARTING:
Start Blender and select RIB Mosaic from Blender's render menu in the info
header (top file bar). Once selected RIB Mosaic will modify Blender's UI,
adding and removing panels as necessary. If RIB Mosaic came packaged with your
renderer it should be setup ready to use. If using a generic copy you'll need
to enable one of the built-in pipelines for your renderer. To do this use any
of the "Pipeline Manager" panels throughout Blender's UI to select and enable
the pipeline for your renderer.

USAGE:
By itself RIB Mosaic only exports RIB, however XML can be used to define whats
exported, executed and shown in the UI. This XML is contained in ".rmp" files
called "pipelines" that can be loaded to extend the exporter's capabilities.
If you installed RIB Mosaic from a render package it most likely came preinstalled
with pipelines to take advantage of that renderer (see their documentation).
If you installed a generic copy of RIB Mosaic it comes with several basic
pipelines to quickly get started with the most popular renderers. To extend the
exporter even further, find and load community made pipelines found in
RIB Mosaic's forums under the "Pipelines and Assets" catagory (see links below).

PRODUCTION:
RIB Mosaic provides a low level C python module to dramatically increase
performance for large complex scenes common in production environments.
See BUILD.txt for instructions on building and installing the ribify module.

INFORMATION:
For more information on using RIB Mosaic see the wiki link in the Add-Ons panel
or by using the links below. If interested in creating your own pipelines please
read through RIB Mosaic's wiki manual under the "Pipeline Development" section.


LINKS:
For the latest news and releases see the SourceForge portal:
<http://sourceforge.net/projects/ribmosaic/>

For references on creating and editing pipelines see the wiki:
<http://sourceforge.net/apps/mediawiki/ribmosaic/>

For help and additional pipelines see the forums:
<http://sourceforge.net/apps/phpbb/ribmosaic/>

Enjoy,
Eric Back (WHiTeRaBBiT)

