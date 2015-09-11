#include seq_C.cpp
#include stdio.h

typedef struct S {
  long sf1;
  sequence sf2;
} S_t;

typedef sequence<S_t> Sseq;
main()
{
   int i,j;
   Sseq seq;      // create an Sseq
   seq.length(3); // set length of seq to 3
   for (i=0; i<3; i++) { // index the three S structs in seq
   seq[i].sf1 = i;    // place a number in the i-indexed struct
   seq[i].sf2.length(i+1); // set length of the sequence in
   //   the i-indexed struct
   for (j=0; j<i+1; j++) // index the i+1 S structs in the sequence
   //  in the i-indexed struct
   seq[i].sf2[j].sf1 = (i+1)*10+j; // place a number in 
   //   the j-indexed struct 
}
// OK. Print out what you have created!
printf("seq = (%d sequence elements)\n", seq.length());
for (i=0; i<3; i++) 
{
   printf("   struct[%d] = {\n", i);
   printf("      sf1 = %d\n", seq[i].sf1);
   printf("      sf2 = (%d sequence elements)\n",
   seq[i].sf2[j].length());
   for (j=0; j<i+1; j++)  
   {
      printf("         struct[%d] = \n",j);
      printf("            sf1 = %d\n", seq[i].sf2[j].sf1);
      printf("            sf2 = (%d sequence elements)\n",
      seq[i].sf2[j].sf2.length());
      printf("         }\n");
      }
   printf("   }\n");
   }
} 
