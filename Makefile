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

local-install:
	@pip install .

local-uninstall:
	@pip uninstall pyvguicom

pip-build:
	./pip-build.py

pip-upload:
	./pip-upload.sh

#@python3 ./install.py

pack:
	@./pack.sh

clean:
	rm -f *.pyc
	rm -rf __pycache__
	rm -rf pyvguicom/__pycache__
	rm -rf build/*
	rm -rf dist/*

git:
	git add .
	git commit -m autocheck
	git push

XPATH=PYTHONPATH=../pyvcommon:../  python -W ignore::DeprecationWarning `which pdoc` --force --html

docs:
	@${XPATH}   -o pyvguicom/docs pyvguicom/pgbox.py
	@${XPATH}   -o pyvguicom/docs pyvguicom/pgsel.py
	@${XPATH}   -o pyvguicom/docs pyvguicom/browsewin.py
	@${XPATH}   -o pyvguicom/docs pyvguicom/pgbutt.py
	@${XPATH}   -o pyvguicom/docs pyvguicom/pgutils.py
	@${XPATH}   -o pyvguicom/docs pyvguicom/pgentry.py
	@${XPATH}   -o pyvguicom/docs pyvguicom/pgwkit.py
	@${XPATH}   -o pyvguicom/docs pyvguicom/pggui.py
	@${XPATH}   -o pyvguicom/docs pyvguicom/pgsimp.py
	@${XPATH}   -o pyvguicom/docs pyvguicom/pggui.py
	@${XPATH}   -o pyvguicom/docs pyvguicom/pgbox.py
	@${XPATH}   -o pyvguicom/docs pyvguicom/pgtextview.py
	@${XPATH}   -o pyvguicom/docs pyvguicom/comline.py
	@${XPATH}   -o pyvguicom/docs pyvguicom/custwidg.py
	@${XPATH}   -o pyvguicom/docs pyvguicom/pgtests.py

# End of Makefile
