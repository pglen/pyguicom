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
	@echo "	 make install    -- Install PyEdPro "
	@echo "	 make pack       -- package PyEdPro "
	@echo

install:
	@python3 ./install.py

pack:
	@./pack.sh

clean:
	rm -f *.pyc
	rm -rf __pycache__

git:
	git add .
	git commit -m autocheck
	git push

docs:
	@pdoc  --force --html -o docs pyvguicom/pgbox.py
	@pdoc  --force --html -o docs pyvguicom/browsewin.py
	@pdoc  --force --html -o docs pyvguicom/pgbutt.py
	@pdoc  --force --html -o docs pyvguicom/pgutils.py
	@pdoc  --force --html -o docs pyvguicom/htmledit.py
	@pdoc  --force --html -o docs pyvguicom/pgentry.py
	@pdoc  --force --html -o docs pyvguicom/pgwkit.py
	@pdoc  --force --html -o docs pyvguicom/sutil.py
	@pdoc  --force --html -o docs pyvguicom/pggui.py
	@pdoc  --force --html -o docs pyvguicom/pgsimp.py
	@pdoc  --force --html -o docs pyvguicom/pggui.py
	@pdoc  --force --html -o docs pyvguicom/pgbox.py
	@pdoc  --force --html -o docs pyvguicom/pgtextview.py

# End of Makefile

# eof
