'''OpenGL extension ARB.vertex_program

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes
EXTENSION_NAME = 'GL_ARB_vertex_program'
_DEPRECATED = False
GL_COLOR_SUM_ARB = constant.Constant( 'GL_COLOR_SUM_ARB', 0x8458 )
glget.addGLGetConstant( GL_COLOR_SUM_ARB, (1,) )
GL_VERTEX_PROGRAM_ARB = constant.Constant( 'GL_VERTEX_PROGRAM_ARB', 0x8620 )
glget.addGLGetConstant( GL_VERTEX_PROGRAM_ARB, (1,) )
GL_VERTEX_ATTRIB_ARRAY_ENABLED_ARB = constant.Constant( 'GL_VERTEX_ATTRIB_ARRAY_ENABLED_ARB', 0x8622 )
GL_VERTEX_ATTRIB_ARRAY_SIZE_ARB = constant.Constant( 'GL_VERTEX_ATTRIB_ARRAY_SIZE_ARB', 0x8623 )
GL_VERTEX_ATTRIB_ARRAY_STRIDE_ARB = constant.Constant( 'GL_VERTEX_ATTRIB_ARRAY_STRIDE_ARB', 0x8624 )
GL_VERTEX_ATTRIB_ARRAY_TYPE_ARB = constant.Constant( 'GL_VERTEX_ATTRIB_ARRAY_TYPE_ARB', 0x8625 )
GL_CURRENT_VERTEX_ATTRIB_ARB = constant.Constant( 'GL_CURRENT_VERTEX_ATTRIB_ARB', 0x8626 )
GL_PROGRAM_LENGTH_ARB = constant.Constant( 'GL_PROGRAM_LENGTH_ARB', 0x8627 )
GL_PROGRAM_STRING_ARB = constant.Constant( 'GL_PROGRAM_STRING_ARB', 0x8628 )
GL_MAX_PROGRAM_MATRIX_STACK_DEPTH_ARB = constant.Constant( 'GL_MAX_PROGRAM_MATRIX_STACK_DEPTH_ARB', 0x862E )
glget.addGLGetConstant( GL_MAX_PROGRAM_MATRIX_STACK_DEPTH_ARB, (1,) )
GL_MAX_PROGRAM_MATRICES_ARB = constant.Constant( 'GL_MAX_PROGRAM_MATRICES_ARB', 0x862F )
glget.addGLGetConstant( GL_MAX_PROGRAM_MATRICES_ARB, (1,) )
GL_CURRENT_MATRIX_STACK_DEPTH_ARB = constant.Constant( 'GL_CURRENT_MATRIX_STACK_DEPTH_ARB', 0x8640 )
glget.addGLGetConstant( GL_CURRENT_MATRIX_STACK_DEPTH_ARB, (1,) )
GL_CURRENT_MATRIX_ARB = constant.Constant( 'GL_CURRENT_MATRIX_ARB', 0x8641 )
glget.addGLGetConstant( GL_CURRENT_MATRIX_ARB, (4,4) )
GL_VERTEX_PROGRAM_POINT_SIZE_ARB = constant.Constant( 'GL_VERTEX_PROGRAM_POINT_SIZE_ARB', 0x8642 )
glget.addGLGetConstant( GL_VERTEX_PROGRAM_POINT_SIZE_ARB, (1,) )
GL_VERTEX_PROGRAM_TWO_SIDE_ARB = constant.Constant( 'GL_VERTEX_PROGRAM_TWO_SIDE_ARB', 0x8643 )
glget.addGLGetConstant( GL_VERTEX_PROGRAM_TWO_SIDE_ARB, (1,) )
GL_VERTEX_ATTRIB_ARRAY_POINTER_ARB = constant.Constant( 'GL_VERTEX_ATTRIB_ARRAY_POINTER_ARB', 0x8645 )
GL_PROGRAM_ERROR_POSITION_ARB = constant.Constant( 'GL_PROGRAM_ERROR_POSITION_ARB', 0x864B )
glget.addGLGetConstant( GL_PROGRAM_ERROR_POSITION_ARB, (1,) )
GL_PROGRAM_BINDING_ARB = constant.Constant( 'GL_PROGRAM_BINDING_ARB', 0x8677 )
GL_MAX_VERTEX_ATTRIBS_ARB = constant.Constant( 'GL_MAX_VERTEX_ATTRIBS_ARB', 0x8869 )
glget.addGLGetConstant( GL_MAX_VERTEX_ATTRIBS_ARB, (1,) )
GL_VERTEX_ATTRIB_ARRAY_NORMALIZED_ARB = constant.Constant( 'GL_VERTEX_ATTRIB_ARRAY_NORMALIZED_ARB', 0x886A )
GL_PROGRAM_ERROR_STRING_ARB = constant.Constant( 'GL_PROGRAM_ERROR_STRING_ARB', 0x8874 )
GL_PROGRAM_FORMAT_ASCII_ARB = constant.Constant( 'GL_PROGRAM_FORMAT_ASCII_ARB', 0x8875 )
GL_PROGRAM_FORMAT_ARB = constant.Constant( 'GL_PROGRAM_FORMAT_ARB', 0x8876 )
GL_PROGRAM_INSTRUCTIONS_ARB = constant.Constant( 'GL_PROGRAM_INSTRUCTIONS_ARB', 0x88A0 )
GL_MAX_PROGRAM_INSTRUCTIONS_ARB = constant.Constant( 'GL_MAX_PROGRAM_INSTRUCTIONS_ARB', 0x88A1 )
GL_PROGRAM_NATIVE_INSTRUCTIONS_ARB = constant.Constant( 'GL_PROGRAM_NATIVE_INSTRUCTIONS_ARB', 0x88A2 )
GL_MAX_PROGRAM_NATIVE_INSTRUCTIONS_ARB = constant.Constant( 'GL_MAX_PROGRAM_NATIVE_INSTRUCTIONS_ARB', 0x88A3 )
GL_PROGRAM_TEMPORARIES_ARB = constant.Constant( 'GL_PROGRAM_TEMPORARIES_ARB', 0x88A4 )
GL_MAX_PROGRAM_TEMPORARIES_ARB = constant.Constant( 'GL_MAX_PROGRAM_TEMPORARIES_ARB', 0x88A5 )
GL_PROGRAM_NATIVE_TEMPORARIES_ARB = constant.Constant( 'GL_PROGRAM_NATIVE_TEMPORARIES_ARB', 0x88A6 )
GL_MAX_PROGRAM_NATIVE_TEMPORARIES_ARB = constant.Constant( 'GL_MAX_PROGRAM_NATIVE_TEMPORARIES_ARB', 0x88A7 )
GL_PROGRAM_PARAMETERS_ARB = constant.Constant( 'GL_PROGRAM_PARAMETERS_ARB', 0x88A8 )
GL_MAX_PROGRAM_PARAMETERS_ARB = constant.Constant( 'GL_MAX_PROGRAM_PARAMETERS_ARB', 0x88A9 )
GL_PROGRAM_NATIVE_PARAMETERS_ARB = constant.Constant( 'GL_PROGRAM_NATIVE_PARAMETERS_ARB', 0x88AA )
GL_MAX_PROGRAM_NATIVE_PARAMETERS_ARB = constant.Constant( 'GL_MAX_PROGRAM_NATIVE_PARAMETERS_ARB', 0x88AB )
GL_PROGRAM_ATTRIBS_ARB = constant.Constant( 'GL_PROGRAM_ATTRIBS_ARB', 0x88AC )
GL_MAX_PROGRAM_ATTRIBS_ARB = constant.Constant( 'GL_MAX_PROGRAM_ATTRIBS_ARB', 0x88AD )
GL_PROGRAM_NATIVE_ATTRIBS_ARB = constant.Constant( 'GL_PROGRAM_NATIVE_ATTRIBS_ARB', 0x88AE )
GL_MAX_PROGRAM_NATIVE_ATTRIBS_ARB = constant.Constant( 'GL_MAX_PROGRAM_NATIVE_ATTRIBS_ARB', 0x88AF )
GL_PROGRAM_ADDRESS_REGISTERS_ARB = constant.Constant( 'GL_PROGRAM_ADDRESS_REGISTERS_ARB', 0x88B0 )
GL_MAX_PROGRAM_ADDRESS_REGISTERS_ARB = constant.Constant( 'GL_MAX_PROGRAM_ADDRESS_REGISTERS_ARB', 0x88B1 )
GL_PROGRAM_NATIVE_ADDRESS_REGISTERS_ARB = constant.Constant( 'GL_PROGRAM_NATIVE_ADDRESS_REGISTERS_ARB', 0x88B2 )
GL_MAX_PROGRAM_NATIVE_ADDRESS_REGISTERS_ARB = constant.Constant( 'GL_MAX_PROGRAM_NATIVE_ADDRESS_REGISTERS_ARB', 0x88B3 )
GL_MAX_PROGRAM_LOCAL_PARAMETERS_ARB = constant.Constant( 'GL_MAX_PROGRAM_LOCAL_PARAMETERS_ARB', 0x88B4 )
GL_MAX_PROGRAM_ENV_PARAMETERS_ARB = constant.Constant( 'GL_MAX_PROGRAM_ENV_PARAMETERS_ARB', 0x88B5 )
GL_PROGRAM_UNDER_NATIVE_LIMITS_ARB = constant.Constant( 'GL_PROGRAM_UNDER_NATIVE_LIMITS_ARB', 0x88B6 )
GL_TRANSPOSE_CURRENT_MATRIX_ARB = constant.Constant( 'GL_TRANSPOSE_CURRENT_MATRIX_ARB', 0x88B7 )
glget.addGLGetConstant( GL_TRANSPOSE_CURRENT_MATRIX_ARB, (4,4) )
GL_MATRIX0_ARB = constant.Constant( 'GL_MATRIX0_ARB', 0x88C0 )
GL_MATRIX1_ARB = constant.Constant( 'GL_MATRIX1_ARB', 0x88C1 )
GL_MATRIX2_ARB = constant.Constant( 'GL_MATRIX2_ARB', 0x88C2 )
GL_MATRIX3_ARB = constant.Constant( 'GL_MATRIX3_ARB', 0x88C3 )
GL_MATRIX4_ARB = constant.Constant( 'GL_MATRIX4_ARB', 0x88C4 )
GL_MATRIX5_ARB = constant.Constant( 'GL_MATRIX5_ARB', 0x88C5 )
GL_MATRIX6_ARB = constant.Constant( 'GL_MATRIX6_ARB', 0x88C6 )
GL_MATRIX7_ARB = constant.Constant( 'GL_MATRIX7_ARB', 0x88C7 )
GL_MATRIX8_ARB = constant.Constant( 'GL_MATRIX8_ARB', 0x88C8 )
GL_MATRIX9_ARB = constant.Constant( 'GL_MATRIX9_ARB', 0x88C9 )
GL_MATRIX10_ARB = constant.Constant( 'GL_MATRIX10_ARB', 0x88CA )
GL_MATRIX11_ARB = constant.Constant( 'GL_MATRIX11_ARB', 0x88CB )
GL_MATRIX12_ARB = constant.Constant( 'GL_MATRIX12_ARB', 0x88CC )
GL_MATRIX13_ARB = constant.Constant( 'GL_MATRIX13_ARB', 0x88CD )
GL_MATRIX14_ARB = constant.Constant( 'GL_MATRIX14_ARB', 0x88CE )
GL_MATRIX15_ARB = constant.Constant( 'GL_MATRIX15_ARB', 0x88CF )
GL_MATRIX16_ARB = constant.Constant( 'GL_MATRIX16_ARB', 0x88D0 )
GL_MATRIX17_ARB = constant.Constant( 'GL_MATRIX17_ARB', 0x88D1 )
GL_MATRIX18_ARB = constant.Constant( 'GL_MATRIX18_ARB', 0x88D2 )
GL_MATRIX19_ARB = constant.Constant( 'GL_MATRIX19_ARB', 0x88D3 )
GL_MATRIX20_ARB = constant.Constant( 'GL_MATRIX20_ARB', 0x88D4 )
GL_MATRIX21_ARB = constant.Constant( 'GL_MATRIX21_ARB', 0x88D5 )
GL_MATRIX22_ARB = constant.Constant( 'GL_MATRIX22_ARB', 0x88D6 )
GL_MATRIX23_ARB = constant.Constant( 'GL_MATRIX23_ARB', 0x88D7 )
GL_MATRIX24_ARB = constant.Constant( 'GL_MATRIX24_ARB', 0x88D8 )
GL_MATRIX25_ARB = constant.Constant( 'GL_MATRIX25_ARB', 0x88D9 )
GL_MATRIX26_ARB = constant.Constant( 'GL_MATRIX26_ARB', 0x88DA )
GL_MATRIX27_ARB = constant.Constant( 'GL_MATRIX27_ARB', 0x88DB )
GL_MATRIX28_ARB = constant.Constant( 'GL_MATRIX28_ARB', 0x88DC )
GL_MATRIX29_ARB = constant.Constant( 'GL_MATRIX29_ARB', 0x88DD )
GL_MATRIX30_ARB = constant.Constant( 'GL_MATRIX30_ARB', 0x88DE )
GL_MATRIX31_ARB = constant.Constant( 'GL_MATRIX31_ARB', 0x88DF )
glVertexAttrib1dARB = platform.createExtensionFunction( 
'glVertexAttrib1dARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,constants.GLdouble,),
doc='glVertexAttrib1dARB(GLuint(index), GLdouble(x)) -> None',
argNames=('index','x',),
deprecated=_DEPRECATED,
)

glVertexAttrib1dvARB = platform.createExtensionFunction( 
'glVertexAttrib1dvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,arrays.GLdoubleArray,),
doc='glVertexAttrib1dvARB(GLuint(index), GLdoubleArray(v)) -> None',
argNames=('index','v',),
deprecated=_DEPRECATED,
)

glVertexAttrib1fARB = platform.createExtensionFunction( 
'glVertexAttrib1fARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,constants.GLfloat,),
doc='glVertexAttrib1fARB(GLuint(index), GLfloat(x)) -> None',
argNames=('index','x',),
deprecated=_DEPRECATED,
)

glVertexAttrib1fvARB = platform.createExtensionFunction( 
'glVertexAttrib1fvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,arrays.GLfloatArray,),
doc='glVertexAttrib1fvARB(GLuint(index), GLfloatArray(v)) -> None',
argNames=('index','v',),
deprecated=_DEPRECATED,
)

glVertexAttrib1sARB = platform.createExtensionFunction( 
'glVertexAttrib1sARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,constants.GLshort,),
doc='glVertexAttrib1sARB(GLuint(index), GLshort(x)) -> None',
argNames=('index','x',),
deprecated=_DEPRECATED,
)

glVertexAttrib1svARB = platform.createExtensionFunction( 
'glVertexAttrib1svARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,arrays.GLshortArray,),
doc='glVertexAttrib1svARB(GLuint(index), GLshortArray(v)) -> None',
argNames=('index','v',),
deprecated=_DEPRECATED,
)

glVertexAttrib2dARB = platform.createExtensionFunction( 
'glVertexAttrib2dARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,constants.GLdouble,constants.GLdouble,),
doc='glVertexAttrib2dARB(GLuint(index), GLdouble(x), GLdouble(y)) -> None',
argNames=('index','x','y',),
deprecated=_DEPRECATED,
)

glVertexAttrib2dvARB = platform.createExtensionFunction( 
'glVertexAttrib2dvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,arrays.GLdoubleArray,),
doc='glVertexAttrib2dvARB(GLuint(index), GLdoubleArray(v)) -> None',
argNames=('index','v',),
deprecated=_DEPRECATED,
)

glVertexAttrib2fARB = platform.createExtensionFunction( 
'glVertexAttrib2fARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,constants.GLfloat,constants.GLfloat,),
doc='glVertexAttrib2fARB(GLuint(index), GLfloat(x), GLfloat(y)) -> None',
argNames=('index','x','y',),
deprecated=_DEPRECATED,
)

glVertexAttrib2fvARB = platform.createExtensionFunction( 
'glVertexAttrib2fvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,arrays.GLfloatArray,),
doc='glVertexAttrib2fvARB(GLuint(index), GLfloatArray(v)) -> None',
argNames=('index','v',),
deprecated=_DEPRECATED,
)

glVertexAttrib2sARB = platform.createExtensionFunction( 
'glVertexAttrib2sARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,constants.GLshort,constants.GLshort,),
doc='glVertexAttrib2sARB(GLuint(index), GLshort(x), GLshort(y)) -> None',
argNames=('index','x','y',),
deprecated=_DEPRECATED,
)

glVertexAttrib2svARB = platform.createExtensionFunction( 
'glVertexAttrib2svARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,arrays.GLshortArray,),
doc='glVertexAttrib2svARB(GLuint(index), GLshortArray(v)) -> None',
argNames=('index','v',),
deprecated=_DEPRECATED,
)

glVertexAttrib3dARB = platform.createExtensionFunction( 
'glVertexAttrib3dARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,constants.GLdouble,constants.GLdouble,constants.GLdouble,),
doc='glVertexAttrib3dARB(GLuint(index), GLdouble(x), GLdouble(y), GLdouble(z)) -> None',
argNames=('index','x','y','z',),
deprecated=_DEPRECATED,
)

glVertexAttrib3dvARB = platform.createExtensionFunction( 
'glVertexAttrib3dvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,arrays.GLdoubleArray,),
doc='glVertexAttrib3dvARB(GLuint(index), GLdoubleArray(v)) -> None',
argNames=('index','v',),
deprecated=_DEPRECATED,
)

glVertexAttrib3fARB = platform.createExtensionFunction( 
'glVertexAttrib3fARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,constants.GLfloat,constants.GLfloat,constants.GLfloat,),
doc='glVertexAttrib3fARB(GLuint(index), GLfloat(x), GLfloat(y), GLfloat(z)) -> None',
argNames=('index','x','y','z',),
deprecated=_DEPRECATED,
)

glVertexAttrib3fvARB = platform.createExtensionFunction( 
'glVertexAttrib3fvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,arrays.GLfloatArray,),
doc='glVertexAttrib3fvARB(GLuint(index), GLfloatArray(v)) -> None',
argNames=('index','v',),
deprecated=_DEPRECATED,
)

glVertexAttrib3sARB = platform.createExtensionFunction( 
'glVertexAttrib3sARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,constants.GLshort,constants.GLshort,constants.GLshort,),
doc='glVertexAttrib3sARB(GLuint(index), GLshort(x), GLshort(y), GLshort(z)) -> None',
argNames=('index','x','y','z',),
deprecated=_DEPRECATED,
)

glVertexAttrib3svARB = platform.createExtensionFunction( 
'glVertexAttrib3svARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,arrays.GLshortArray,),
doc='glVertexAttrib3svARB(GLuint(index), GLshortArray(v)) -> None',
argNames=('index','v',),
deprecated=_DEPRECATED,
)

glVertexAttrib4NbvARB = platform.createExtensionFunction( 
'glVertexAttrib4NbvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,arrays.GLbyteArray,),
doc='glVertexAttrib4NbvARB(GLuint(index), GLbyteArray(v)) -> None',
argNames=('index','v',),
deprecated=_DEPRECATED,
)

glVertexAttrib4NivARB = platform.createExtensionFunction( 
'glVertexAttrib4NivARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,arrays.GLintArray,),
doc='glVertexAttrib4NivARB(GLuint(index), GLintArray(v)) -> None',
argNames=('index','v',),
deprecated=_DEPRECATED,
)

glVertexAttrib4NsvARB = platform.createExtensionFunction( 
'glVertexAttrib4NsvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,arrays.GLshortArray,),
doc='glVertexAttrib4NsvARB(GLuint(index), GLshortArray(v)) -> None',
argNames=('index','v',),
deprecated=_DEPRECATED,
)

glVertexAttrib4NubARB = platform.createExtensionFunction( 
'glVertexAttrib4NubARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,constants.GLubyte,constants.GLubyte,constants.GLubyte,constants.GLubyte,),
doc='glVertexAttrib4NubARB(GLuint(index), GLubyte(x), GLubyte(y), GLubyte(z), GLubyte(w)) -> None',
argNames=('index','x','y','z','w',),
deprecated=_DEPRECATED,
)

glVertexAttrib4NubvARB = platform.createExtensionFunction( 
'glVertexAttrib4NubvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,arrays.GLubyteArray,),
doc='glVertexAttrib4NubvARB(GLuint(index), GLubyteArray(v)) -> None',
argNames=('index','v',),
deprecated=_DEPRECATED,
)

glVertexAttrib4NuivARB = platform.createExtensionFunction( 
'glVertexAttrib4NuivARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,arrays.GLuintArray,),
doc='glVertexAttrib4NuivARB(GLuint(index), GLuintArray(v)) -> None',
argNames=('index','v',),
deprecated=_DEPRECATED,
)

glVertexAttrib4NusvARB = platform.createExtensionFunction( 
'glVertexAttrib4NusvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,arrays.GLushortArray,),
doc='glVertexAttrib4NusvARB(GLuint(index), GLushortArray(v)) -> None',
argNames=('index','v',),
deprecated=_DEPRECATED,
)

glVertexAttrib4bvARB = platform.createExtensionFunction( 
'glVertexAttrib4bvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,arrays.GLbyteArray,),
doc='glVertexAttrib4bvARB(GLuint(index), GLbyteArray(v)) -> None',
argNames=('index','v',),
deprecated=_DEPRECATED,
)

glVertexAttrib4dARB = platform.createExtensionFunction( 
'glVertexAttrib4dARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,constants.GLdouble,constants.GLdouble,constants.GLdouble,constants.GLdouble,),
doc='glVertexAttrib4dARB(GLuint(index), GLdouble(x), GLdouble(y), GLdouble(z), GLdouble(w)) -> None',
argNames=('index','x','y','z','w',),
deprecated=_DEPRECATED,
)

glVertexAttrib4dvARB = platform.createExtensionFunction( 
'glVertexAttrib4dvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,arrays.GLdoubleArray,),
doc='glVertexAttrib4dvARB(GLuint(index), GLdoubleArray(v)) -> None',
argNames=('index','v',),
deprecated=_DEPRECATED,
)

glVertexAttrib4fARB = platform.createExtensionFunction( 
'glVertexAttrib4fARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,constants.GLfloat,constants.GLfloat,constants.GLfloat,constants.GLfloat,),
doc='glVertexAttrib4fARB(GLuint(index), GLfloat(x), GLfloat(y), GLfloat(z), GLfloat(w)) -> None',
argNames=('index','x','y','z','w',),
deprecated=_DEPRECATED,
)

glVertexAttrib4fvARB = platform.createExtensionFunction( 
'glVertexAttrib4fvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,arrays.GLfloatArray,),
doc='glVertexAttrib4fvARB(GLuint(index), GLfloatArray(v)) -> None',
argNames=('index','v',),
deprecated=_DEPRECATED,
)

glVertexAttrib4ivARB = platform.createExtensionFunction( 
'glVertexAttrib4ivARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,arrays.GLintArray,),
doc='glVertexAttrib4ivARB(GLuint(index), GLintArray(v)) -> None',
argNames=('index','v',),
deprecated=_DEPRECATED,
)

glVertexAttrib4sARB = platform.createExtensionFunction( 
'glVertexAttrib4sARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,constants.GLshort,constants.GLshort,constants.GLshort,constants.GLshort,),
doc='glVertexAttrib4sARB(GLuint(index), GLshort(x), GLshort(y), GLshort(z), GLshort(w)) -> None',
argNames=('index','x','y','z','w',),
deprecated=_DEPRECATED,
)

glVertexAttrib4svARB = platform.createExtensionFunction( 
'glVertexAttrib4svARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,arrays.GLshortArray,),
doc='glVertexAttrib4svARB(GLuint(index), GLshortArray(v)) -> None',
argNames=('index','v',),
deprecated=_DEPRECATED,
)

glVertexAttrib4ubvARB = platform.createExtensionFunction( 
'glVertexAttrib4ubvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,arrays.GLubyteArray,),
doc='glVertexAttrib4ubvARB(GLuint(index), GLubyteArray(v)) -> None',
argNames=('index','v',),
deprecated=_DEPRECATED,
)

glVertexAttrib4uivARB = platform.createExtensionFunction( 
'glVertexAttrib4uivARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,arrays.GLuintArray,),
doc='glVertexAttrib4uivARB(GLuint(index), GLuintArray(v)) -> None',
argNames=('index','v',),
deprecated=_DEPRECATED,
)

glVertexAttrib4usvARB = platform.createExtensionFunction( 
'glVertexAttrib4usvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,arrays.GLushortArray,),
doc='glVertexAttrib4usvARB(GLuint(index), GLushortArray(v)) -> None',
argNames=('index','v',),
deprecated=_DEPRECATED,
)

glVertexAttribPointerARB = platform.createExtensionFunction( 
'glVertexAttribPointerARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,constants.GLint,constants.GLenum,constants.GLboolean,constants.GLsizei,ctypes.c_void_p,),
doc='glVertexAttribPointerARB(GLuint(index), GLint(size), GLenum(type), GLboolean(normalized), GLsizei(stride), c_void_p(pointer)) -> None',
argNames=('index','size','type','normalized','stride','pointer',),
deprecated=_DEPRECATED,
)

glEnableVertexAttribArrayARB = platform.createExtensionFunction( 
'glEnableVertexAttribArrayARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,),
doc='glEnableVertexAttribArrayARB(GLuint(index)) -> None',
argNames=('index',),
deprecated=_DEPRECATED,
)

glDisableVertexAttribArrayARB = platform.createExtensionFunction( 
'glDisableVertexAttribArrayARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,),
doc='glDisableVertexAttribArrayARB(GLuint(index)) -> None',
argNames=('index',),
deprecated=_DEPRECATED,
)

glProgramStringARB = platform.createExtensionFunction( 
'glProgramStringARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLenum,constants.GLenum,constants.GLsizei,ctypes.c_void_p,),
doc='glProgramStringARB(GLenum(target), GLenum(format), GLsizei(len), c_void_p(string)) -> None',
argNames=('target','format','len','string',),
deprecated=_DEPRECATED,
)

glBindProgramARB = platform.createExtensionFunction( 
'glBindProgramARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLenum,constants.GLuint,),
doc='glBindProgramARB(GLenum(target), GLuint(program)) -> None',
argNames=('target','program',),
deprecated=_DEPRECATED,
)

glDeleteProgramsARB = platform.createExtensionFunction( 
'glDeleteProgramsARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLsizei,arrays.GLuintArray,),
doc='glDeleteProgramsARB(GLsizei(n), GLuintArray(programs)) -> None',
argNames=('n','programs',),
deprecated=_DEPRECATED,
)

glGenProgramsARB = platform.createExtensionFunction( 
'glGenProgramsARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLsizei,arrays.GLuintArray,),
doc='glGenProgramsARB(GLsizei(n), GLuintArray(programs)) -> None',
argNames=('n','programs',),
deprecated=_DEPRECATED,
)

glProgramEnvParameter4dARB = platform.createExtensionFunction( 
'glProgramEnvParameter4dARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLenum,constants.GLuint,constants.GLdouble,constants.GLdouble,constants.GLdouble,constants.GLdouble,),
doc='glProgramEnvParameter4dARB(GLenum(target), GLuint(index), GLdouble(x), GLdouble(y), GLdouble(z), GLdouble(w)) -> None',
argNames=('target','index','x','y','z','w',),
deprecated=_DEPRECATED,
)

glProgramEnvParameter4dvARB = platform.createExtensionFunction( 
'glProgramEnvParameter4dvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLenum,constants.GLuint,arrays.GLdoubleArray,),
doc='glProgramEnvParameter4dvARB(GLenum(target), GLuint(index), GLdoubleArray(params)) -> None',
argNames=('target','index','params',),
deprecated=_DEPRECATED,
)

glProgramEnvParameter4fARB = platform.createExtensionFunction( 
'glProgramEnvParameter4fARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLenum,constants.GLuint,constants.GLfloat,constants.GLfloat,constants.GLfloat,constants.GLfloat,),
doc='glProgramEnvParameter4fARB(GLenum(target), GLuint(index), GLfloat(x), GLfloat(y), GLfloat(z), GLfloat(w)) -> None',
argNames=('target','index','x','y','z','w',),
deprecated=_DEPRECATED,
)

glProgramEnvParameter4fvARB = platform.createExtensionFunction( 
'glProgramEnvParameter4fvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLenum,constants.GLuint,arrays.GLfloatArray,),
doc='glProgramEnvParameter4fvARB(GLenum(target), GLuint(index), GLfloatArray(params)) -> None',
argNames=('target','index','params',),
deprecated=_DEPRECATED,
)

glProgramLocalParameter4dARB = platform.createExtensionFunction( 
'glProgramLocalParameter4dARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLenum,constants.GLuint,constants.GLdouble,constants.GLdouble,constants.GLdouble,constants.GLdouble,),
doc='glProgramLocalParameter4dARB(GLenum(target), GLuint(index), GLdouble(x), GLdouble(y), GLdouble(z), GLdouble(w)) -> None',
argNames=('target','index','x','y','z','w',),
deprecated=_DEPRECATED,
)

glProgramLocalParameter4dvARB = platform.createExtensionFunction( 
'glProgramLocalParameter4dvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLenum,constants.GLuint,arrays.GLdoubleArray,),
doc='glProgramLocalParameter4dvARB(GLenum(target), GLuint(index), GLdoubleArray(params)) -> None',
argNames=('target','index','params',),
deprecated=_DEPRECATED,
)

glProgramLocalParameter4fARB = platform.createExtensionFunction( 
'glProgramLocalParameter4fARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLenum,constants.GLuint,constants.GLfloat,constants.GLfloat,constants.GLfloat,constants.GLfloat,),
doc='glProgramLocalParameter4fARB(GLenum(target), GLuint(index), GLfloat(x), GLfloat(y), GLfloat(z), GLfloat(w)) -> None',
argNames=('target','index','x','y','z','w',),
deprecated=_DEPRECATED,
)

glProgramLocalParameter4fvARB = platform.createExtensionFunction( 
'glProgramLocalParameter4fvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLenum,constants.GLuint,arrays.GLfloatArray,),
doc='glProgramLocalParameter4fvARB(GLenum(target), GLuint(index), GLfloatArray(params)) -> None',
argNames=('target','index','params',),
deprecated=_DEPRECATED,
)

glGetProgramEnvParameterdvARB = platform.createExtensionFunction( 
'glGetProgramEnvParameterdvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLenum,constants.GLuint,arrays.GLdoubleArray,),
doc='glGetProgramEnvParameterdvARB(GLenum(target), GLuint(index), GLdoubleArray(params)) -> None',
argNames=('target','index','params',),
deprecated=_DEPRECATED,
)

glGetProgramEnvParameterfvARB = platform.createExtensionFunction( 
'glGetProgramEnvParameterfvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLenum,constants.GLuint,arrays.GLfloatArray,),
doc='glGetProgramEnvParameterfvARB(GLenum(target), GLuint(index), GLfloatArray(params)) -> None',
argNames=('target','index','params',),
deprecated=_DEPRECATED,
)

glGetProgramLocalParameterdvARB = platform.createExtensionFunction( 
'glGetProgramLocalParameterdvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLenum,constants.GLuint,arrays.GLdoubleArray,),
doc='glGetProgramLocalParameterdvARB(GLenum(target), GLuint(index), GLdoubleArray(params)) -> None',
argNames=('target','index','params',),
deprecated=_DEPRECATED,
)

glGetProgramLocalParameterfvARB = platform.createExtensionFunction( 
'glGetProgramLocalParameterfvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLenum,constants.GLuint,arrays.GLfloatArray,),
doc='glGetProgramLocalParameterfvARB(GLenum(target), GLuint(index), GLfloatArray(params)) -> None',
argNames=('target','index','params',),
deprecated=_DEPRECATED,
)

glGetProgramivARB = platform.createExtensionFunction( 
'glGetProgramivARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLenum,constants.GLenum,arrays.GLintArray,),
doc='glGetProgramivARB(GLenum(target), GLenum(pname), GLintArray(params)) -> None',
argNames=('target','pname','params',),
deprecated=_DEPRECATED,
)

glGetProgramStringARB = platform.createExtensionFunction( 
'glGetProgramStringARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLenum,constants.GLenum,ctypes.c_void_p,),
doc='glGetProgramStringARB(GLenum(target), GLenum(pname), c_void_p(string)) -> None',
argNames=('target','pname','string',),
deprecated=_DEPRECATED,
)

glGetVertexAttribdvARB = platform.createExtensionFunction( 
'glGetVertexAttribdvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,constants.GLenum,arrays.GLdoubleArray,),
doc='glGetVertexAttribdvARB(GLuint(index), GLenum(pname), GLdoubleArray(params)) -> None',
argNames=('index','pname','params',),
deprecated=_DEPRECATED,
)

glGetVertexAttribfvARB = platform.createExtensionFunction( 
'glGetVertexAttribfvARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,constants.GLenum,arrays.GLfloatArray,),
doc='glGetVertexAttribfvARB(GLuint(index), GLenum(pname), GLfloatArray(params)) -> None',
argNames=('index','pname','params',),
deprecated=_DEPRECATED,
)

glGetVertexAttribivARB = platform.createExtensionFunction( 
'glGetVertexAttribivARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,constants.GLenum,arrays.GLintArray,),
doc='glGetVertexAttribivARB(GLuint(index), GLenum(pname), GLintArray(params)) -> None',
argNames=('index','pname','params',),
deprecated=_DEPRECATED,
)

glGetVertexAttribPointervARB = platform.createExtensionFunction( 
'glGetVertexAttribPointervARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,constants.GLenum,ctypes.POINTER(ctypes.c_void_p),),
doc='glGetVertexAttribPointervARB(GLuint(index), GLenum(pname), POINTER(ctypes.c_void_p)(pointer)) -> None',
argNames=('index','pname','pointer',),
deprecated=_DEPRECATED,
)

glIsProgramARB = platform.createExtensionFunction( 
'glIsProgramARB',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=constants.GLboolean, 
argTypes=(constants.GLuint,),
doc='glIsProgramARB(GLuint(program)) -> constants.GLboolean',
argNames=('program',),
deprecated=_DEPRECATED,
)


def glInitVertexProgramARB():
    '''Return boolean indicating whether this extension is available'''
    return extensions.hasGLExtension( EXTENSION_NAME )
