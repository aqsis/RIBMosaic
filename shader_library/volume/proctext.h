/* I took wave's lead and renamed proctexh.h to DPProctext.h -- tal@cs.caltech.edu */

/*
 * Preprocessor macros for use in RenderMan shaders.
 * Darwyn Peachey, June, 1994.
 *
 * removing redundant functions and adding correct includes.
 * 2006-03-13 dan@3-e.net
 * as you can see this file is redundant and all inludes that use it need to 
 * be change to call the two below.
 */
#include "noises.h"
#include "functions.h"

/* Not used in any *.sl file, refer to pulse(a,b,fuzz,x) in rmannotes.h
 *
 * #define PULSE(a,b,x) (step((a),(x)) - step((b),(x)))
 *
 */
