{
  description = "Identity Provider Development Environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    cursor-arm.url = "github:coder/cursor-arm";
  };

  outputs = { self, nixpkgs, flake-utils, cursor-arm, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            appimage-run
            python3
            python3Packages.pip
            python3Packages.virtualenv
          ];
          
          CURSOR_PATH = "${cursor-arm.packages.${system}.cursor.linux.arm64-appimage}";
          shellHook = ''
            source venv/bin/activate
          '';
        };
      }
    );
}
