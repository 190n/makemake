#!/usr/bin/python3

from collections import defaultdict

use_cpp = input('C++? [yN] ').lower() == 'y'
objects = input('object files: ').split()
binaries = input('binaries: ').split()

for i, o in enumerate(objects):
	print(f'  {i}: {o}')

objs_per_bin = defaultdict(lambda: [])
for b in binaries:
	prompt = f'object files for {b}'
	if f'{b}.o' in objects:
		objs_per_bin[b].append(f'{b}.o')
		prompt += f' (+ {b}.o)'

	objs_per_bin[b] += map(lambda i: objects[int(i)], input(f'{prompt}: ').split())

with open('Makefile', 'w') as fp:
	if use_cpp:
		fp.write(('CC = clang++\n'
		          'CFLAGS = -std=c++17 -Wall -Wextra -Werror -Wpedantic -O2 -g\n'
		          'LFLAGS =\n\n'))
	else:
		fp.write(('CC = clang\n'
		          'CFLAGS = -std=c17 -Wall -Wextra -Werror -Wpedantic -O2 -g\n'
		          'LFLAGS =\n\n'))

	for b in binaries:
		fp.write(f'{b}_OBJS = {" ".join(objs_per_bin[b])}\n')

	fp.write(('\n'
	         f'all: {" ".join(binaries)}\n'
	         '\n'
	        f'%.o: %.{"cpp" if use_cpp else "c"}\n'
	         '\t$(CC) $(CFLAGS) -c $<\n'
	         '\n'))

	for b in binaries:
		fp.write((f'{b}: {" ".join(objs_per_bin[b])}\n'
		          f'\t$(CC) $(LFLAGS) $({b}_OBJS) -o {b}\n'
		           '\n'))

	for b in binaries:
		fp.write((f'check{b}: {b}\n'
		          f'\tvalgrind --leak-check=full ./{b}\n'
		           '\n'))

	fp.write(('clean:\n'
	         f'\trm -f *.o'))
	for f in binaries:
		fp.write(f' {f}')

	fp.write(('\n'
	          '\n'
	          'scan-build: clean\n'
	          '\tscan-build --use-cc=$(CC) make all\n'
	          '\n'
	          'format:\n'
	          '\tclang-format -i -style=file *.[ch]\n'
	          '\n'
	         f'.PHONY: all clean scan-build format {" ".join(map(lambda b: f"check{b}", binaries))}\n'))
