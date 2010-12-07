Welcome to RIB Mosaic!

INTRODUCTION:
This repository is primarily targeted for developers wanting to test the latest
versions of RIB Mosiac, customize their own Add-Ons or compile the ribify module
for production use.

INSTALLATION:
If looking for a stable ready made Add-On please use the downloads from
<http://sourceforge.net/projects/ribmosaic/files/>, otherwise you can find
instructions for installing an Add-On from this repository in README.txt in the
"render_ribmosaic" folder.

CUSTOMIZATION:
RIB Mosaic has been designed to be easily customized and re-distributed for any
RenderMan rendering package. This is accomplished by passing near total control
of code export, execution and the UI to pipelines. The following outlines the
basic steps for building your own Blender Add-On using RIB Mosaic as the core
exporter...

- Develop a suite of pipelines that setup all basic functionality of the target
  renderer. This is the hardest part of the process as pipeline development can
  require a wide range of programming skills. When developing your suite also
  keep in mind that advanced renderer functionality can always be downloaded
  and installed separately as the user requires them.
  For more information please refer to "Pipeline Development" in the wiki manual.
- Copy the "render_ribmosaic" folder and rename it to reflect the name and
  purpose of your package.
- Replace all .rmp files in the "pipelines" folder with your pipeline suite.
  Pipelines contained in this folder will be automatically loaded in new blends.
- To further customize your Add-On, edit the "bl_addon_info" dictionary in
  RIB Mosaic's __init__.py script to change the displayed name, version and links.
  Keep in mind that each Add-On will require a unique folder and name in order
  to co-exist with other RIB Mosaic Add-Ons. Since this project is under the
  GPL license your free to make any modifications your project requires, however
  I recommend keeping all changes in __init__.py as this file will likely remain
  untouched in future revisions.
- Once you've added all pipelines and modified __init__.py simply compress your
  folder into a zip archive for distribution and instruct your users on how to
  install it (see the README.txt for standard installation instructions).

PRODUCTION:
RIB Mosaic provides a low level C python module to dramatically increase
performance for large complex scenes common in production environments.
See BUILD.txt in "render_ribmosaic" for instructions on building and installing
the ribify module.

Enjoy,
Eric Back (WHiTeRaBBiT)
