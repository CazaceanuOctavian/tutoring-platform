{
  description = "Development environment with Python, Node.js, and local PostgreSQL";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        name = "tutoring_platform";
        pkgs = import nixpkgs { inherit system; };

        pythonEnv = pkgs.python312.withPackages (ps: with ps; [
          fastapi
          fastapi-cli
          requests
	  aiohttp
          psycopg2
          asyncpg
          sqlalchemy
	  sqlmodel
          jupyter
          notebook
          pip
          ipython
          scipy
          matplotlib
          seaborn
        ]);
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            pythonEnv

            # Node / frontend
            pkgs.nodejs_22

            # PostgreSQL
            pkgs.postgresql_15
            pkgs.pgcli

            # Build deps
            pkgs.gcc
            pkgs.gnumake
            pkgs.openssl
            pkgs.pkg-config
            pkgs.cyrus_sasl
          ];

          LOCALE_ARCHIVE =
            if pkgs.stdenv.isLinux
            then "${pkgs.glibcLocales}/lib/locale/locale-archive"
            else "";

         shellHook = ''
            ############################################################
            # Project-scoped directories
            ############################################################
            export NIX_SHELL_DIR="$PWD/.nix-shell"
            export PGDATA="$NIX_SHELL_DIR/postgres"
            export PGHOST="$PGDATA"
            export PGPORT=5432
            export PGUSER=$(whoami)
            export PGDATABASE=${name}

            mkdir -p "$NIX_SHELL_DIR"

            ############################################################
            # Cleanup on exit
            ############################################################
            trap "
              if pg_ctl -D \"$PGDATA\" status > /dev/null 2>&1; then
                echo 'Stopping PostgreSQL...'
                pg_ctl -D \"$PGDATA\" stop
              fi
            " EXIT

            ############################################################
            # Initialize database if needed
            ############################################################
            if [ ! -d "$PGDATA" ]; then
              echo 'Initializing PostgreSQL database...'
              pg_ctl initdb -D "$PGDATA"

              # Development-only auth (INSECURE)
              sed -i "s/^host\s\+all\s\+all\s\+127.0.0.1\/32.*/host all all 0.0.0.0\/0 trust/" "$PGDATA/pg_hba.conf"
              sed -i "s/^host\s\+all\s\+all\s\+::1\/128.*/host all all ::\/0 trust/" "$PGDATA/pg_hba.conf"
            fi

            ############################################################
            # Start PostgreSQL
            ############################################################
            if ! pg_ctl -D "$PGDATA" status > /dev/null 2>&1; then
              echo 'Starting PostgreSQL...'
              pg_ctl \
                -D "$PGDATA" \
                -l "$PGDATA/postgres.log" \
                -o "-c unix_socket_directories=$PGDATA" \
                -o "-c listen_addresses=*" \
                -o "-c logging_collector=on" \
                start
            fi

            ############################################################
            # Create database if missing
            ############################################################
            if ! psql -lqt | cut -d \| -f 1 | grep -qw "$PGDATABASE"; then
              createdb "$PGDATABASE"
            fi

            ############################################################
            # Python pip local install support
            ############################################################
            export PIP_PREFIX="$PWD/_build/pip_packages"
            export PYTHONPATH="$PIP_PREFIX/${pkgs.python312.sitePackages}:$PYTHONPATH"
            export PATH="$PIP_PREFIX/bin:$PATH"
            unset SOURCE_DATE_EPOCH

            ############################################################
            # Frontend deps bootstrap (optional)
            ############################################################
            if [ ! -d "dependency/node_modules" ]; then
              npm install --prefix dependency vite react
              echo "Vite + React installed"
            fi

            echo
            echo "======================================"
            echo "Dev environment ready"
            echo "PostgreSQL:"
            echo "  PGDATA=$PGDATA"
            echo "  Database=$PGDATABASE"
            echo "  Socket=$PGDATA"
            echo
            echo "Connect with:"
            echo "  psql $PGDATABASE"
            echo "======================================"
          '';
        };
      }
    );
}

