*Task:*

- A library of functions for working with m-bit integers has been developed. The library must support numbers up to 2048 bits long.
The following operations were implemented:
  1) conversion of small constants into the format of a large number (in particular, 0 and 1);
  2) adding numbers;
  3) subtraction of numbers;
  4) multiplication of numbers, raising numbers to the square;
  5) division of numbers, finding the remainder from division;
  6) raising a number to a multi-digit power;
  7) converting (translating) a number into a character string and the reverse conversion of a character string into a number; hexadecimal representation is mandatory, decimal and binary are preferred.

- Calculated average execution time of implemented arithmetic operations.

For each operation, the execution time was measured using the time.process_time() function, before and after each operation. Then, the difference between the post-execution time and the pre-execution time was added to the total execution time of each operation. The total time obtained was divided by 1000, since 1000 measurements were taken

The number of processor cycles for each operation is calculated using the formula:
number of clocks = execution time (seconds) * clock frequency (Hz)
The clock frequency of my computer is 2.50GHz, that is 2500000000Hz


| Operation | Average execution time (seconds) | The number of processor cycles |
|-----------------------|-----------------------|-----------------------|
| Addition | 0,0000012 | 3000 |
| Subtraction | 0,0000013 | 3250 |
| Multiplication | 0,0000027 | 6750 |
| Division | 0,0000031 | 7750 |
| Reminder from division | 0,0000034 | 8500 |
| Exponentiation | 0,0000029 | 7250 |
