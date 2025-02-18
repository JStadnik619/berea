benchmark:
	hyperfine --warmup 3 'python3 -m biblecli.cli Genesis 3 3'