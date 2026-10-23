# Build Windows artifacts on branches and release tags from main

Every branch push builds the three Windows executables and uploads them as workflow artifacts so changes can be tried before release. Version tags publish a GitHub Release and the Python package only when the tagged commit is in `main`'s history and the executable build succeeds. This keeps preview builds available from development branches while reserving public releases for code that has reached `main`, even though the repository's default branch is `develop`.
