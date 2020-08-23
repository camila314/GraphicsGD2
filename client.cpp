#include <gdstdlib.hpp>
#include <GDML/GDML.hpp>
#include <CoreFoundation/CoreFoundation.h>
#include "b64.hpp"

typedef void(*queuefunc)(std::string);
GameManager* sharedManager;
std::vector<std::pair<queuefunc, std::string>> thequeue;
ModContainer* loop;

void mainLoop(void* instance) {
	if(thequeue.size()) {
		thequeue[0].first(thequeue[0].second);

		thequeue.erase(thequeue.begin());
	}
	return FCAST(mainLoop, loop->getOriginal(getBase()+0x249690))(instance);
}


void pasteObjects(std::string objs) {
		if(auto layer = static_cast<LevelEditorLayer*>(sharedManager->valOffset(0x188))) {
			auto editor = static_cast<EditorUI*>(layer->valOffset(0x5d8));
			editor->pasteObjects(objs);
		}
}
void clearLevel(std::string none) {
		if(auto layer = static_cast<LevelEditorLayer*>(sharedManager->valOffset(0x188))) {
			auto editor = static_cast<EditorUI*>(layer->valOffset(0x5d8));
			layer->removeAllObjects();
		}
}
void undo(std::string none) {
		if(auto layer = static_cast<LevelEditorLayer*>(sharedManager->valOffset(0x188))) {
			auto editor = static_cast<EditorUI*>(layer->valOffset(0x5d8));
			editor->undoLastAction();
		}
}
void redo(std::string none) {
		if(auto layer = static_cast<LevelEditorLayer*>(sharedManager->valOffset(0x188))) {
			auto editor = static_cast<EditorUI*>(layer->valOffset(0x5d8));
			editor->redoLastAction();
		}
}
void popup(std::string data) {
	auto list = split(data, ',');

	std::string title;
	std::string desc;
	std::string button;

	b64::Base64::Decode(list[0], title);
	b64::Base64::Decode(list[1], desc);
	b64::Base64::Decode(list[2], button);

	auto alert = FLAlertLayer::create(NULL, title.c_str(), desc, button.c_str(), NULL, 300.0);
	alert->show();


}

static CFDataRef Callback(CFMessagePortRef port,
						  SInt32 messageID,
						  CFDataRef data,
						  void *info) {

	if(!CFDataGetLength(data))
		return NULL;

	std::string cdata(reinterpret_cast<char const*>(CFDataGetBytePtr(data)));

	cdata.resize(CFDataGetLength(data));


	switch(messageID) {
		case 1: // add object
			thequeue.push_back(std::make_pair(pasteObjects, cdata));
			break;
		case 2: // clear level
			thequeue.push_back(std::make_pair(clearLevel,std::string("")));
			break;
		case 3: // undo
			thequeue.push_back(std::make_pair(undo,std::string("")));
			break;
		case 4: // redo
			thequeue.push_back(std::make_pair(redo,std::string("")));
			break;
		case 5: //popup
			thequeue.push_back(std::make_pair(popup,cdata));
			break;

	}
	return NULL;
}

void initIPC() {
	CFMessagePortRef localPort = CFMessagePortCreateLocal(NULL,
								 CFSTR("314GDL"),
								 Callback,
								 NULL,
								 NULL);
	CFRunLoopSourceRef runLoopSource = CFMessagePortCreateRunLoopSource(NULL, localPort, 0);

	CFRunLoopAddSource(CFRunLoopGetCurrent(),
					   runLoopSource,
					   kCFRunLoopCommonModes);
	CFRunLoopRun();
	CFRelease(localPort);
}
void inject() {
	sharedManager = GameManager::sharedState();

	loop = new ModContainer("GraphicsGD Loop", "global");
	loop->registerHook(getBase()+0x249690,(func_t)mainLoop);

	loop->enable();

	initIPC();
}