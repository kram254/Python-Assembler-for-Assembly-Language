.data
str:  .asciiz "\nHello World!\n"

.text
.globl main

main:

li $t0, 30
# You can change the 20 below to another value
li $t1, 20

# Now we can add the values in $t0
# and $t1, putting the result in special register $a0
add $a0, $t0, $t1

# Set up for printing the value in $a0.
# A 1 in $v0 means we want to print an integer
li $v0, 1

# The system call looks at what is in $v0
# and $a0, and knows to print what is in $a0
syscall

# Now we want to print Hello World
# So we load the (address of the) string into $a0.
# The address of the string is too big to be stored
# by one instruction, so we first load the upper half,
# shift it across, then load the lower half
la $a0, str

# And put a 4 in $v0 to mean print a string
li $v0, 4

# And just like before syscall looks at
# $v0 and $a0 and knows to print the string
syscall

# Nicely end the program
li $v0, 0
jr $ra
  