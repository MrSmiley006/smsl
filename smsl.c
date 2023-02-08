#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
	if (argc == 1 || argc > 3) {
		printf("Použití: smsl.exe <název programu> [-p]\n");
		printf("<> - povinný parametr, [] - nepovinný parametr\n");
		return 1;
	}
	//argv[0] = ' ';
	char command[100] = "python\\python.exe smsl.py ";
	strcat(command, argv[1]);
	if (argc == 3) {
		strcat(command, " ");
		strcat(command, argv[2]);
	}
	system(command);
	
}