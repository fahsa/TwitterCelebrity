import os, sys, shutil

def main():
	if os.path.exists('testUser/'):
		shutil.rmtree('testUser/')

	if os.path.exists('char_output'):
		os.remove('char_output')

	if os.path.exists('rocchio.out'):
		os.remove('rocchio.out')

	if os.path.exists('word_output'):
		os.remove('word_output')

	if os.path.exists('nn_output'):
		os.remove('nn_output')

if __name__ == '__main__':
	main()