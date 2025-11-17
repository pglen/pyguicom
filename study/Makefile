INCX=$(shell pkg-config  --cflags   gtk+-3.0)
INCX+=$(shell pkg-config --cflags  glib-2.0)

LIBX=$(shell pkg-config  --libs gtk+-3.0)
LIBX+=$(shell pkg-config --libs glib-2.0)

psock:
	@#echo $(INCX) $(LIBX)
	gcc psock.c -o psock $(INCX) $(LIBX)

 #  eof