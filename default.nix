{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = pkgs.python311.withPackages (ps: with ps; [ 
#    pydantic_1_10_5
#    anyio_3_6_2
#    fastapi_0_92_0
#    idna_3_4_0 
#    sniffio_1_3_0
#    starlette_0_25_0 
    pydantic
    anyio
    fastapi
    idna 
    sniffio
    starlette 
]);
in
pythonEnv
