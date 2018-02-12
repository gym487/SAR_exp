      #include<stdio.h>
      #include<stdlib.h>
      int main(int argc, char *argv[])
      {
           int i;
           printf("These are the %d   command- line   arguments passed   to main:\n\n", argc);
           for(i=0; i<=argc; i++)
             printf("argv[%d]:%s\n", i, argv[i]);
           printf("\nThe environment string(s)on this system are:\n\n");
	return 0;
      }
