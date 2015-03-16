scss ?= assets/_sass/styles.scss
css ?= assets/css/styles.css

all: styles

styles:
	sass $(scss):$(css)

watch:
	sass --watch $(scss):$(css)

clean:
	rm -f $(css)
