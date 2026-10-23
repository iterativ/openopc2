# Third-party assets

The MIT License in [LICENSE.txt](LICENSE.txt) applies to project-authored code
and documentation. It does not grant rights to the following bundled assets,
which remain subject to their respective owners' terms:

- `lib/gbda_aut.dll` — Graybox OPC DA Automation Wrapper. An [archived Graybox
  product page](https://web.archive.org/web/20240920163619id_/http://gray-box.net/daawrapper.php?lang=en)
  permits free use and redistribution with products; it does not make the DLL
  MIT licensed.
- `lib/api-ms-win-core-path-l1-1-0.dll` — a Microsoft Windows DLL. Permission
  to redistribute this exact file independently has not been established.
- `lib/x64/OPC Core Components Redistributable (x64).msi` — OPC Foundation Core
  Components. The [current package](https://opcfoundation.org/developer-tools/samples-and-tools-classic/core-components/)
  is under the OPC MIT license, but its terms have not been verified for this
  older MSI. The [2017 redistributables agreement](https://opcfoundation.org/license/redistributables/1.3/)
  has additional distribution conditions.
- `doc/OpenOPC.pdf` — legacy OpenOPC documentation with no explicit license
  notice found in the document.
- `scripts/graybox_opc_automation_wrapper.py` — code generated from the
  Graybox type library; the Graybox product page does not expressly address
  this generated source file.

See [the file-specific research](docs/research/third-party-license-research.md)
for provenance and evidence. The permissions for the Microsoft DLL, older OPC
MSI, legacy PDF, and generated Python file need confirmation before
redistribution.
