import datetime
import subprocess
import sys

import yaml


def main():
	mkdocs_yml = read_mkdocs_yml()
	chapters = make_chapter_list(mkdocs_yml)

	pandoc_command = 'docker run --rm -v "$(pwd):/data" -u $(id -u):$(id -g) pandoc/extra --template eisvogel'
	chapters_list = ' '.join(chapters)
	output_file = make_output_file_name()
	subprocess.run(f'{pandoc_command} {chapters_list} -o {output_file}', shell=True, cwd='docs/master_plan')

	blob_url = f'https://storageaccountportab0da.blob.core.windows.net/public-assets/master_plan/{output_file}'
	subprocess.run(
		f'az storage blob upload --auth-mode login -f {output_file} --blob-url {blob_url} --overwrite',
		shell=True,
		cwd='docs/master_plan')

	print(f'Uploaded to {blob_url}')


def read_mkdocs_yml():
	def default_ctor(loader, tag_suffix, node):
		return None

	yaml.add_multi_constructor('', default_ctor, Loader=yaml.SafeLoader)
	with open('mkdocs.yml', 'r') as f:
		return yaml.load(f, yaml.SafeLoader)


def make_chapter_list(mkdocs_yml):
	nav = mkdocs_yml['nav']
	master_plan = [item for item in nav if 'Master Plan' in item][0]
	prefix_len = len('master_plan/')
	chapters = [c[prefix_len:] for c in master_plan['Master Plan']]
	chapters = ['meta.md'] + chapters
	print(chapters)
	return chapters


def make_output_file_name():
	try:
		suffix = sys.argv[1]
	except IndexError:
		suffix = None

	date = datetime.datetime.now().strftime('%Y-%m-%d')
	if suffix:
		return f'master_plan_{date}_{suffix}.pdf'
	else:
		return f'master_plan_{date}.pdf'


if __name__ == '__main__':
	main()
