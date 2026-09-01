# Third-Party Notices

This file lists the main third-party Python components that are directly
referenced by this repository's source files, `environment.yml`, and build
files as of 2026-04-02.

This file is a practical notice file for the source repository. If you
distribute a frozen application, installer, or any other external package, you
should review the exact contents of the shipped bundle and expand this document
for all bundled transitive dependencies, Qt modules, fonts, icons, manuals,
and other third-party materials actually distributed.

This file is informational only and does not modify any third-party license.

## License Texts

Full license texts for components whose licenses require them to be distributed
alongside the software are provided in the `licenses/` directory:

| File | Applies to |
| --- | --- |
| `licenses/LGPL-3.0.txt` | PySide6 / Qt (LGPLv3) |
| `licenses/GPL-3.0.txt` | Incorporated by reference into LGPLv3 |
| `licenses/OFL-1.1.txt` | Roboto font (SIL Open Font License 1.1) |
| `licenses/Apache-2.0.txt` | PyInstaller (portions under Apache-2.0) |

MIT and BSD license texts are reproduced in the appendices at the end of this
file.

## Summary

| Component | Use in this repository | License | Upstream / Source |
| --- | --- | --- | --- |
| `PySide6` | GUI, Qt Widgets, QML, translation, settings | Qt for Python Community Edition: LGPLv3 / GPLv3; commercial edition also available | https://doc.qt.io/qtforpython-6/commercial/index.html |
| `pyqtgraph` | Real-time graph rendering | MIT | https://github.com/pyqtgraph/pyqtgraph/blob/master/LICENSE.txt |
| `pandas` | Tabular and log data handling | BSD 3-Clause | https://github.com/pandas-dev/pandas/blob/main/LICENSE |
| `numpy` | Numerical array processing | BSD 3-Clause | https://github.com/numpy/numpy/blob/main/LICENSE.txt |
| `scipy` | FFT and signal processing | BSD 3-Clause | https://github.com/scipy/scipy/blob/main/LICENSE.txt |
| `pyserial` | Serial port enumeration and communication | BSD 3-Clause | https://github.com/pyserial/pyserial/blob/master/LICENSE.txt |
| `pyinstaller` | Build / packaging tool | GPL-2.0-or-later with bootloader exception; some files under Apache-2.0 | https://pyinstaller.org/en/stable/license.html |
| `bottleneck` | Hidden import declared in `Hiz-mil.spec` | Simplified BSD / BSD-2-Clause | https://github.com/pydata/bottleneck/blob/master/LICENSE |
| `Roboto` font | Bundled in `Views/fonts/` and embedded in `Views/resources_rc.py` for UI text rendering | SIL Open Font License 1.1 | https://github.com/googlefonts/roboto-classic |
| `Feather Icons` | Some UI icons in `Views/Images/` (e.g. `refresh-ccw.png`, `camera.png`, `download.png`, `upload.png`, `pause.png`), obtained via Figma's built-in icon assets | MIT | https://github.com/feathericons/feather/blob/main/LICENSE |
| `Ionicons` | Some UI icons in `Views/Images/` (e.g. `close-sharp.png`, `help-circle-sharp.png`, `information-circle-sharp.png`, `options-outline.png`), obtained via Figma's built-in icon assets | MIT | https://github.com/ionic-team/ionicons/blob/main/LICENSE |

## Notes by Component

### PySide6

- Repository usage: imported throughout `Controllers/`, `Views/`, `Models/`,
  and `Utils/`. Confirmed submodules actually used in this repository are
  `QtCore`, `QtGui`, `QtWidgets`, `QtQuickWidgets`, and, from QML,
  `QtQuick`, `QtQuick.Controls`, `QtQuick.Layouts`, `QtQuick.Effects`, and
  `QtQuick.Controls.Material`. These are all Qt Essentials modules; this
  repository does not use any GPL-only/commercial-only Qt Add-on modules
  (e.g. Qt Charts, Qt 3D, Qt WebEngine, Qt Virtual Keyboard).
- Official Qt for Python documentation states that Qt for Python follows Qt's
  licensing model and provides a Community Edition under LGPLv3 / GPLv3, plus
  a Commercial Edition.
- Official Qt documentation also states that some Qt parts and third-party
  code can carry additional license terms.
- Inference: because this repository declares `pyside6` in `environment.yml`
  and only uses Qt Essentials modules, it is intended to use the
  LGPLv3-licensed open-source/community distribution; purchasing a separate
  commercial Qt license is not required for this repository's usage. The
  LGPLv3 permits commercial and closed-source use of the Application that
  links against the Library; it does not require this repository's own code
  to be licensed under LGPLv3/GPLv3.
- License text: this repository does not reproduce the full text of the GNU
  Lesser General Public License v3.0 here. The authoritative, permanent copy
  is published by the Free Software Foundation at:
  - LGPLv3: https://www.gnu.org/licenses/lgpl-3.0.html
  - GPLv3 (incorporated by reference into LGPLv3): https://www.gnu.org/licenses/gpl-3.0.html
- Source availability: PySide6 and Qt are open source. Corresponding source
  code for the exact PySide6/Qt version used can be obtained from:
  - PySide6 source distributions on PyPI: https://pypi.org/project/PySide6/#files
  - Qt for Python source repository: https://code.qt.io/cgit/pyside/pyside-setup.git/
  - Qt official source releases: https://download.qt.io/official_releases/qt/
- Build note: `Hiz-mil.spec` builds with PyInstaller's `COLLECT` (one-folder)
  mode rather than a single-file bundle, so the PySide6/Qt shared libraries
  ship as separate, replaceable files alongside the application executable
  rather than being merged into one binary.
- Build note: `Hiz-mil.spec` collects PySide6/Qt as separate files in a
  one-directory (`COLLECT`) bundle rather than merging everything into a
  single file, which keeps the Library replaceable as contemplated by LGPLv3
  section 4(d)(1).
- The full text of LGPLv3 is provided in `licenses/LGPL-3.0.txt`. LGPLv3
  incorporates GNU GPLv3 by reference; the full GPLv3 text is provided in
  `licenses/GPL-3.0.txt`. Both files are included in source and binary
  distributions of this software, alongside the PySide6/Qt libraries.

Official references:

- Qt for Python commercial / community licensing:
  https://doc.qt.io/qtforpython-6/commercial/index.html
- Licenses used in Qt for Python:
  https://doc.qt.io/qtforpython-6/licenses.html
- General Qt licensing:
  https://doc.qt.io/qt-6/licensing.html
- LGPLv3 full text: https://www.gnu.org/licenses/lgpl-3.0.txt
- GPLv3 full text: https://www.gnu.org/licenses/gpl-3.0.txt

### Feather Icons

Repository usage:

- Some small UI icons under `Views/Images/` (e.g. `refresh-ccw.png`,
  `camera.png`, `download.png`, `upload.png`, `pause.png`, `filter.png`,
  `zoom-in.png`, `zoom-out.png`) match Feather Icons' naming convention and
  were obtained via Figma's built-in default icon assets.

Copyright notice:

Copyright (c) 2013-2023 Cole Bemis

License:

MIT License. See "Appendix A - MIT License Text" below.

Official source:

https://github.com/feathericons/feather/blob/main/LICENSE

### Ionicons

Repository usage:

- Some small UI icons under `Views/Images/` (e.g. `close-sharp.png`,
  `help-circle-sharp.png`, `information-circle-sharp.png`,
  `options-outline.png`, `refresh-sharp.png`, `save-sharp.png`) match
  Ionicons' `-sharp` / `-outline` naming convention and were obtained via
  Figma's built-in default icon assets.

Copyright notice:

Copyright (c) 2015-present Ionic (http://ionic.io/)

License:

MIT License. See "Appendix A - MIT License Text" below.

Official source:

https://github.com/ionic-team/ionicons/blob/main/LICENSE

### Roboto

Copyright notice:

Copyright 2011 The Roboto Project Authors
(https://github.com/googlefonts/roboto-classic)

Roboto is a trademark of Google.

License:

SIL Open Font License, Version 1.1. The full text is provided in
`licenses/OFL-1.1.txt`.

Notes:

- The font file `Views/fonts/Roboto-VariableFont_wdth,wght.ttf` is present in
  this repository and is also embedded into `Views/resources_rc.py` through
  `Views/resources.qrc`. The application loads it at run time with
  `QFontDatabase.addApplicationFont(":/fonts/fonts/Roboto-VariableFont_wdth,wght.ttf")`
  in `Controllers/MainController.py`.
- The license recorded in the font file's own `name` table (name IDs 13 and 14)
  is the SIL Open Font License 1.1. Older Roboto releases were distributed
  under the Apache License 2.0; the file bundled here is an OFL-licensed
  release, so OFL 1.1 is the applicable license.
- OFL 1.1 section 2 requires that each copy of the Font Software is accompanied
  by the copyright notice above and by the license text. Source and binary
  distributions of this software satisfy this by shipping `licenses/OFL-1.1.txt`
  together with this notices file.
- No Reserved Font Name is declared for this font.

Official source:

https://github.com/googlefonts/roboto-classic

### pyqtgraph

Copyright notice:

Copyright (c) 2012 University of North Carolina at Chapel Hill

Luke Campagnola

License:

MIT License. See "Appendix A - MIT License Text" below.

Official source:

https://github.com/pyqtgraph/pyqtgraph/blob/master/LICENSE.txt

### pandas

Copyright notice:

Copyright (c) 2008-2011, AQR Capital Management, LLC, Lambda Foundry, Inc. and
PyData Development Team. All rights reserved.

Copyright (c) 2011-2026, Open source contributors.

License:

BSD 3-Clause License. See "Appendix B - BSD 3-Clause License Text" below.

Official source:

https://github.com/pandas-dev/pandas/blob/main/LICENSE

### numpy

Copyright notice:

Copyright (c) 2005-2025, NumPy Developers. All rights reserved.

License:

BSD 3-Clause License. See "Appendix B - BSD 3-Clause License Text" below.

Official source:

https://github.com/numpy/numpy/blob/main/LICENSE.txt

### scipy

Copyright notice:

Copyright (c) 2001-2002 Enthought, Inc.

Copyright (c) 2003, SciPy Developers.

All rights reserved.

License:

BSD 3-Clause License. See "Appendix B - BSD 3-Clause License Text" below.

Official source:

https://github.com/scipy/scipy/blob/main/LICENSE.txt

### pyserial

Copyright notice:

Copyright (c) 2001-2020 Chris Liechti

All Rights Reserved.

License:

BSD 3-Clause License. See "Appendix B - BSD 3-Clause License Text" below.

Official source:

https://github.com/pyserial/pyserial/blob/master/LICENSE.txt

### pyinstaller

Repository usage:

- Declared in `environment.yml`
- Used by `Hiz-mil.spec`, `Hiz-mil.exe.spec`, `Hiz-mil_linux.spec`,
  and `build_mac.sh`

Primary notice:

Copyright (c) 2010-2023, PyInstaller Development Team

Copyright (c) 2005-2009, Giovanni Bajo

Based on previous work under copyright (c) 2002 McMillan Enterprises, Inc.

License summary:

- PyInstaller's official documentation describes PyInstaller as using GPL 2.0
  with an exception for the bootloader, and Apache License 2.0 for certain
  files.
- The same official documentation states that executable bundles generated
  from your source code can be shipped under your own license, provided you
  comply with the licenses of your dependencies.

Official references:

- PyInstaller license overview:
  https://pyinstaller.org/en/stable/license.html
- PyInstaller source license file:
  https://raw.githubusercontent.com/pyinstaller/pyinstaller/develop/COPYING.txt

### bottleneck

Repository usage:

- Declared as a hidden import in `Hiz-mil.spec`

Copyright notice:

Copyright (c) 2010-2019 Keith Goodman

Copyright (c) 2019 Bottleneck Developers

All rights reserved.

License:

Simplified BSD / BSD-2-Clause License. See "Appendix C - BSD 2-Clause
License Text" below.

Official sources:

- https://github.com/pydata/bottleneck/blob/master/LICENSE
- https://pypi.org/project/Bottleneck/

## Appendix A - MIT License Text

MIT License

Copyright (c) 2012 University of North Carolina at Chapel Hill

Luke Campagnola

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Appendix B - BSD 3-Clause License Text

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## Appendix C - BSD 2-Clause License Text

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
