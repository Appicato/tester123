#pragma once
#include "Patterns.h"
#include "../MetinPythonLib/defines.h"
#include <map>


#define STR(x) #x


std::map<int, Pattern> memPatterns = {
	{PYTHONAPP_PROCESS,Pattern(STR(PYTHONAPP_PROCESS), 0, "\x55\x8b\xec\x6a\x00\x68\x00\x00\x00\x00\x64\xa1\x00\x00\x00\x00\x50\x81\xec\x00\x00\x00\x00\xa1\x00\x00\x00\x00\x33\xc5\x50\x8d\x45\x00\x64\xa3\x00\x00\x00\x00\x89\x8d\x00\x00\x00\x00\xe8\x00\x00\x00\x00\x0f\xb6", "xxxx?x????xx????xxx????x????xxxxx?xx????xx????x????xx")},
	{BACKGROUND_CHECKADVANCING,Pattern(STR(BACKGROUND_CHECKADVANCING), 0, "\x55\x8b\xec\x6a\x00\x68\x00\x00\x00\x00\x64\xa1\x00\x00\x00\x00\x50\x83\xec\x00\xa1\x00\x00\x00\x00\x33\xc5\x50\x8d\x45\x00\x64\xa3\x00\x00\x00\x00\x89\x4d\x00\x8b\x4d\x00\xe8\x00\x00\x00\x00\x0f\xb6\x00\x85\xc0\x75\x00\xb0", "xxxx?x????xx????xxx?x????xxxxx?xx????xx?xx?x????xx?xxx?x")},
	{INSTANCE_CHECKADVANCING,Pattern(STR(INSTANCE_CHECKADVANCING), 0, "\x55\x8b\xec\x81\xec\x00\x00\x00\x00\x89\x8d\x00\x00\x00\x00\x8b\x8d\x00\x00\x00\x00\xe8\x00\x00\x00\x00\x0f\xb6\x00\x85\xc0\x0f\x85", "xxxxx????xx????xx????x????xx?xxxx") },

	//From CPythonCharacterManager::Instance()
	{CHRACTERMANAGER_POINTER,Pattern(STR(CHRACTERMANAGER_POINTER), 4, "\x89\x55\x00\xa1\x00\x00\x00\x00\x89\x45\x00\x8b\x4d\x00\xe8\x00\x00\x00\x00\x89\x45\x00\x83\x7d", "xx?x????xx?xx?x????xx?xx")},

	//Search for string CPythonPlayer::__OnPressItem, go to caller of that functionand find the __OnPressGround function,and a reference will be inside
	{INSTANCEBASE_MOVETODEST,Pattern(STR(INSTANCEBASE_MOVETODEST), 0, "\x55\x8b\xec\x83\xec\x00\x89\x4d\x00\x8d\x45\x00\x50\x8b\x4d\x00\xe8\x00\x00\x00\x00\x8b\x4d", "xxxxx?xx?xx?xxx?x????xx")},
	{PYTHONPLAYER_SENDUSESKILL,Pattern(STR(PYTHONPLAYER_SENDUSESKILL), 0, "\x55\x8b\xec\x83\xec\x00\x89\x4d\x00\x8b\x45\x00\x6b\xc0\x00\x8b\x4d\x00\x8d\x94\x01\x00\x00\x00\x00\x89\x55\x00\xa1\x00\x00\x00\x00\x89\x45\x00\x8b\x4d", "xxxxx?xx?xx?xx?xx?xxx????xx?x????xx?xx")},
	{TRACENF_POINTER,Pattern(STR(TRACENF_POINTER), 0, "\x81\xec\x00\x00\x00\x00\xa1\x00\x00\x00\x00\x33\xc4\x89\x84\x24\x00\x00\x00\x00\x8b\x8c\x24\x00\x00\x00\x00\x8d\x84\x24\x00\x00\x00\x00\x50\x51\x8d\x54\x24\x00\x68\x00\x00\x00\x00\x52\xe8\x00\x00\x00\x00\x83\xc4\x00\x85\xc0", "xx????x????xxxxx????xxx????xxx????xxxxx?x????xx????xx?xx")},
	{TRACEF_POINTER,Pattern(STR(TRACEF_POINTER), 0, "\x81\xec\x00\x00\x00\x00\xa1\x00\x00\x00\x00\x33\xc4\x89\x84\x24\x00\x00\x00\x00\x8b\x8c\x24\x00\x00\x00\x00\x8d\x84\x24\x00\x00\x00\x00\x50\x51\x8d\x54\x24\x00\x68\x00\x00\x00\x00\x52\xe8\x00\x00\x00\x00\x83\xc4\x00\x83\x3d", "xx????x????xxxxx????xxx????xxx????xxxxx?x????xx????xx?xx")},
	{GLOBALTOLOCAL_FUNCTION,Pattern(STR(GLOBALTOLOCAL_FUNCTION), 0, "\xe8\x00\x00\x00\x00\x8d\x4d\x00\xe8\x00\x00\x00\x00\x0f\xb6\x4d", "x????xx?x????xxx")},
	{LOCALTOGLOBAL_FUNCTION,Pattern(STR(LOCALTOGLOBAL_FUNCTION), 0, "\x55\x8b\xec\x83\xec\x00\x89\x4d\x00\xa1\x00\x00\x00\x00\x89\x45\x00\x8b\x4d\x00\x51\x8b\x55\x00\x52\x8b\x4d\x00\xe8\x00\x00\x00\x00\x8b\xe5\x5d\xc2\x00\x00\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\x55\x8b\xec\x83\xec\x00\x89\x4d\x00\xa1\x00\x00\x00\x00\x89\x45\x00\x8b\x4d\x00\xe8", "xxxxx?xx?x????xx?xx?xxx?xxx?x????xxxx??xxxxxxxxxxxxxx?xx?x????xx?xx?x")},

	{MOVETODIRECTION_FUNCTION,Pattern(STR(MOVETODIRECTION_FUNCTION), 0, "\x55\x8b\xec\x83\xec\x00\x89\x4d\x00\x8b\x4d\x00\xe8\x00\x00\x00\x00\x0f\xb6\x00\x85\xc0\x74\x00\xb0", "xxxxx?xx?xx?x????xx?xxx?x")},
	//SendExchangeStartPacket 
	//{GLOBAL_PATTERN,Pattern(STR(GLOBAL_PATTERN), 0, "\x55\x8b\xec\x83\xec\x00\x89\x4d\x00\xc6\x45\x00\x00\x8d\x45\x00\x50\x8b\x4d\x00\xe8\x00\x00\x00\x00\x0f\xb6\x00\x85\xc9\x75\x00\x32\xc0\xe9\x00\x00\x00\x00\x8b\x4d\x00\xe8\x00\x00\x00\x00\x0f\xb6\x00\x85\xd2\x75\x00\xb0\x00\xeb\x00\x8d\x45\x00\x89\x45\x00\x8b\x4d\x00\xc6\x01\x00\xba\x00\x00\x00\x00\x8b\x45\x00\x66\x89\x50\x00\x6a\x00\x6a\x00\x8d\x4d\x00\x51\xe8\x00\x00\x00\x00\x83\xc4\x00\xc6\x45\x00\x00\xc6\x45\x00\x00\x8b\x55", "xxxxx?xx?xx??xx?xxx?x????xx?xxx?xxx????xx?x????xx?xxx?x?x?xx?xx?xx?xx?x????xx?xxx?x?x?xx?xx????xx?xx??xx??xx")},

	{SEND_FUNCTION,Pattern(STR(SEND_FUNCTION), 0, "\x56\x8b\xf1\x8b\x46\x00\x8b\x4e\x00\x57\x8b\x7c\x24", "xxxxx?xx?xxxx")},
	{SENDSEQUENCE_FUNCTION,Pattern(STR(SENDSEQUENCE_FUNCTION), 0, "\x51\x56\x8b\xf1\x80\xbe\x00\x00\x00\x00\x00\x75", "xxxxxx?????x")},
	//{RECV_FUNCTION,Pattern(STR(RECV_FUNCTION), 0, "\x8b\x44\x24\x00\x56\x57\x8b\x7c\x24\x00\x50", "xxx?xxxxx?x") },

	//RELATIVE CPYTHONNETWORK
	{RECV_FUNCTION,Pattern(STR(RECV_FUNCTION), 0, "\xe8\x00\x00\x00\x00\x0f\xb6\x00\x85\xc9\x75\x00\x32\xc0\xe9\x00\x00\x00\x00\x8d\x55\x00\x52\x6a","x????xx?xxx?xxx????xx?xx") },

	{GETETHER_FUNCTION,Pattern(STR(GETETHER_FUNCTION), 0, "\x56\x8b\xf1\x83\x7e\x00\x00\x57\x75\x00\x8b\x7c\x24", "xxxxx??xx?xxx") },

	//Pattern from Send On_Click Packet caller
	{NETWORKCLASS_POINTER,Pattern(STR(NETWORKCLASS_POINTER), 4, "\x6a\x00\x8b\x0d\x00\x00\x00\x00\xe8\x00\x00\x00\x00\x8b\x55\x00\x83\xc2", "x?xx????x????xx?xx") },

	//CPythonPlayer Gathered from playerRegisterCacheEffect
	{PYTHONPLAYER_POINTER,Pattern(STR(PYTHONPLAYER_POINTER), 1, "\xa1\x00\x00\x00\x00\x89\x45\x00\x6a\x00\x8b\x4d\x00\x51\x8b\x55\x00\x52\x8b\x4d\x00\xe8\x00\x00\x00\x00\x0f\xb6", "x????xx?x?xx?xxx?xxx?x????xx")},
	{SENDATTACK_FUNCTION,Pattern(STR(SENDATTACK_FUNCTION), 0, "\x55\x8b\xec\x83\xec\x00\x89\x4d\x00\xc6\x45\x00\x00\x8d\x45\x00\x50\x8b\x4d\x00\xe8\x00\x00\x00\x00\x0f\xb6\x00\x85\xc9\x75\x00\x32\xc0\xeb\x00\x8b\x4d\x00\xe8\x00\x00\x00\x00\x0f\xb6\x00\x85\xd2\x75\x00\xb0\x00\xeb\x00\xc6\x45\x00\x00\x8a\x45\x00\x88\x45\x00\x8b\x4d", "xxxxx?xx?xx??xx?xxx?x????xx?xxx?xxx?xx?x????xx?xxx?x?x?xx??xx?xx?xx")},
	{SENDSHOOT_FUNCTION,Pattern(STR(SENDSHOOT_FUNCTION), 0, "\x55\x8b\xec\x83\xec\x00\x89\x4d\x00\xc6\x45\x00\x00\x8d\x45\x00\x50\x8b\x4d\x00\xe8\x00\x00\x00\x00\x0f\xb6\x00\x85\xc9\x75\x00\x32\xc0\xeb\x00\x8b\x4d\x00\xe8\x00\x00\x00\x00\x0f\xb6\x00\x85\xd2\x74\x00\xb0\x00\xeb\x00\xc6\x45\x00\x00\x8a\x45\x00\x88\x45\x00\x8d\x4d", "xxxxx?xx?xx??xx?xxx?x????xx?xxx?xxx?xx?x????xx?xxx?x?x?xx??xx?xx?xx")},
	{SENDCHARACTERSTATE_FUNCTION,Pattern(STR(SENDCHARACTERSTATE_FUNCTION), 0, "\x55\x8b\xec\x83\xec\x00\x89\x4d\x00\xc6\x45\x00\x00\x8d\x45\x00\x50\x8b\x4d\x00\xe8\x00\x00\x00\x00\x0f\xb6\x00\x85\xc9\x75\x00\x32\xc0\xe9\x00\x00\x00\x00\x8b\x4d\x00\xe8\x00\x00\x00\x00\x0f\xb6\x00\x85\xd2\x75\x00\xb0\x00\xe9\x00\x00\x00\x00\xd9\x45", "xxxxx?xx?xx??xx?xxx?x????xx?xxx?xxx????xx?x????xx?xxx?x?x????xx")},
	{RENDER_MID_FUNCTION,Pattern(STR(RENDER_MID_FUNCTION),0,"\x74\x00\xc7\x05\x00\x00\x00\x00\x00\x00\x00\x00\x83\x3d\x00\x00\x00\x00\x00\x0f\x85", "x?xx????????xx?????xx")},

	//CPythonNetwork
	{CHECK_PACKET_FUNCTION,Pattern(STR(CHECK_PACKET_FUNCTION),0,"\x55\x8b\xec\x6a\x00\x68\x00\x00\x00\x00\x64\xa1\x00\x00\x00\x00\x50\x83\xec\x00\xa1\x00\x00\x00\x00\x33\xc5\x50\x8d\x45\x00\x64\xa3\x00\x00\x00\x00\x89\x4d\x00\x8b\x45\x00\xc6\x00","xxxx?x????xx????xxx?x????xxxxx?xx????xx?xx?xx") },
	
	//CPythonNetwork - relative
	{PEEK_FUNCTION,Pattern(STR(PEEK_FUNCTION),0,"\xe8\x00\x00\x00\x00\x0f\xb6\x00\x85\xc9\x75\x00\x32\xc0\xe9\x00\x00\x00\x00\x0f\xb6\x55\x00\x85\xd2\x75\x00\x8d\x45","x????xx?xxx?xxx????xxx?xxx?xx")}
};

