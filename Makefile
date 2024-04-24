#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
#  FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
#  WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

.PHONY: docs

all:
	@echo "Targets: git install pack docs clean ; 'make help' for a full list."

help:
	@echo
	@echo "Targets:"
	@echo "	 make install    -- Install  "
	@echo "	 make pack       -- package  "
	@echo

install:
	@python3 ./install.py

pack:
	@./pack.sh

clean:
	rm -f *.pyc
	rm -rf __pycache__
	rm -rf build/*
	rm -rf dist/*

git:
	git add .
	git commit -m autocheck
	git push

XPATH=PYTHONPATH=../pyvcommon:../  python -W ignore::DeprecationWarning `which pdoc` --force --html

docs:
	@${XPATH}   -o docs pyvguicom/pgbox.py
	@${XPATH}   -o docs pyvguicom/pgsel.py
	@${XPATH}   -o docs pyvguicom/browsewin.py
	@${XPATH}   -o docs pyvguicom/pgbutt.py
	@${XPATH}   -o docs pyvguicom/pgutils.py
	@${XPATH}   -o docs pyvguicom/htmledit.py
	@${XPATH}   -o docs pyvguicom/pgentry.py
	@${XPATH}   -o docs pyvguicom/pgwkit.py
	@${XPATH}   -o docs pyvguicom/sutil.py
	@${XPATH}   -o docs pyvguicom/pggui.py
	@${XPATH}   -o docs pyvguicom/pgsimp.py
	@${XPATH}   -o docs pyvguicom/pggui.py
	@${XPATH}   -o docs pyvguicom/pgbox.py
	@${XPATH}   -o docs pyvguicom/pgtextview.py

# End of Makefile

# eof
