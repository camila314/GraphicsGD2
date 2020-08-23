main:
	colorgcc client.cpp -std=c++11 -lstdc++ -lc++ -lgdstdlib -lGDML -dynamiclib -I/usr/local/include/cocos2dx -I/usr/local/include/cocos2dext -o client.dylib -framework CoreFoundation
inj:
	sudo osxinj "Geometry Dash" client.dylib