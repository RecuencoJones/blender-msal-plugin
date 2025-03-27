set dotenv-load

source_directory := "src"
blender := env('BLENDER_BIN', 'blender')

[private]
default:
	@just --list

venv:
	[ -d .venv ] || uv venv --seed

install-dependencies *UV-ARGS: venv
	uv sync --all-groups {{ UV-ARGS }}

setup: venv install-dependencies download-dependencies

[private]
download-wheels platform:
	uv run pip download \
		-r ./{{source_directory}}/wheels/requirements.txt \
		--dest ./{{source_directory}}/wheels \
		--only-binary=:all: \
		--python-version=$(cat .python-version) \
		--platform={{platform}}

[private]
download-wheel dependency platform:
	uv run pip download {{dependency}} \
		--dest ./{{source_directory}}/wheels \
		--only-binary=:all: \
		--python-version=$(cat .python-version) \
		--platform={{platform}}

download-dependencies: venv
	uv export -q --frozen --no-hashes --no-group dev -o ./{{source_directory}}/wheels/requirements.txt
	just download-wheels macosx_14_0_x86_64
	just download-wheels macosx_14_0_arm64
	just download-wheels win_amd64
	just download-wheel pymsalruntime==0.17.1 macosx_14_0_x86_64
	just download-wheel pymsalruntime==0.17.1 macosx_14_0_arm64
	just download-wheel pymsalruntime==0.17.1 win_amd64

build-plugin:
	{{ blender }} --background --factory-startup --command extension build --source-dir {{ source_directory }}

install-plugin: build-plugin
	-{{ blender }} --command extension remove msal
	{{ blender }} --command extension install-file -r user_default -e msal-0.1.0.zip
