with import <nixpkgs> { };

let
  custom_py = python39.withPackages (python-packages:
    with python-packages; [
      discordpy
      toml
    ]);
in stdenv.mkDerivation {
  name = "custom_py-dev-environment";
  buildInputs = [ custom_py ];
}
