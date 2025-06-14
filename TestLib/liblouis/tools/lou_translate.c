/* liblouis Braille Translation and Back-Translation Library

   Based on the Linux screenreader BRLTTY, copyright (C) 1999-2006 by
   The BRLTTY Team

   Copyright (C) 2004, 2005, 2006, 2009
   ViewPlus Technologies, Inc. www.viewplus.com and
   JJB Software, Inc. www.jjb-software.com
   Copyright (C) 2024 Swiss Library for the Blind, Visually Impaired and Print Disabled

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <config.h>

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <getopt.h>
#include "liblouis.h"
#include "internal.h"
#include "progname.h"
#include "unistr.h"
#include "version-etc.h"

const char version_etc_copyright[] =
		"Copyright %s %d ViewPlus Technologies, Inc. and JJB Software, Inc.";

#define AUTHORS "John J. Boyer"

static void
translate_input(int forward_translation, char *table_name, char *display_table_name,
		int mode, FILE *input) {
	char charbuf[MAXSTRING];
	uint8_t *outputbuf;
	size_t outlen;
	widechar inbuf[MAXSTRING];
	widechar transbuf[MAXSTRING];
	int inlen;
	int translen;
	int k;
	int ch = 0;
	int result;
	while (1) {
		translen = MAXSTRING;
		k = 0;
		while ((ch = fgetc(input)) != '\n' && ch != EOF && k < MAXSTRING - 1)
			charbuf[k++] = ch;
		if (ch == EOF && k == 0) break;
		charbuf[k] = 0;
		inlen = _lou_extParseChars(charbuf, inbuf);
		if (forward_translation)
			result = _lou_translate(table_name, display_table_name, inbuf, &inlen,
					transbuf, &translen, NULL, NULL, NULL, NULL, NULL, mode, NULL, NULL);
		else
			result = _lou_backTranslate(table_name, display_table_name, inbuf, &inlen,
					transbuf, &translen, NULL, NULL, NULL, NULL, NULL, mode, NULL, NULL);
		if (!result) break;
#ifdef WIDECHARS_ARE_UCS4
		outputbuf = u32_to_u8(transbuf, translen, NULL, &outlen);
#else
		outputbuf = u16_to_u8(transbuf, translen, NULL, &outlen);
#endif
		printf(ch == EOF ? "%.*s" : "%.*s\n", (int)outlen, outputbuf);
		free(outputbuf);
	}
}

// copied from metadata.c
static int
isValidChar(char c) {
	return (c >= '0' && c <= '9') || (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') ||
			c == '-' || c == '.' || c == '_';
}

static void
print_help(void) {
	printf("\
Usage: %s [OPTIONS] TABLE\n\n",
			program_name);

	fputs("\
Translate whatever is on standard input and print it on standard\n\
output. It is intended for large-scale testing of the accuracy of\n\
braille translation and back-translation.\n\n",
			stdout);

	fputs("\
TABLE is either:\n\
  - a query           KEY[:VALUE] [KEY[:VALUE] ...]\n\
  - a file list       FILE[,FILE,...]\n\n",
			stdout);

	fputs("\
Options:\n\
  -h, --help           display this help and exit\n\
  -v, --version        display version information and exit\n\
  -f, --forward        forward translation using the given table\n\
  -b, --backward       backward translation using the given table\n\
                       If neither -f nor -b are specified forward translation\n\
                       is assumed\n\
  -d, --display-table  use the given display table for the translation. This\n\
                       is useful when you are specifying the table as a query.\n\
                       This option takes precedence over any display table\n\
                       specified as part of the table file list.\n",
			stdout);
	fputs("\
Examples:\n\
  lou_translate language:en grade:2 region:en-US < input.txt\n\
  \n\
  Do a forward translation of English text to grade 2 contracted braille\n\
  according to the U.S. braille standard.\n\
  \n\
  lou_translate --forward en-us-g2.ctb < input.txt\n\
  \n\
  Do a forward translation with table en-us-g2.ctb.\n\
  \n\
  lou_translate unicode.dis,en-us-g2.ctb < input.txt\n\
  \n\
  If you require a specific braille encoding use a display table. Here we do a\n\
  forward translation with table en-us-g2.ctb and a display table for Unicode\n\
  braille. The resulting braille is encoded as Unicode dot patterns.\n\
  \n\
  lou_translate -d unicode.dis language:en grade:2 region:en-US < input.txt\n\
  \n\
  Using a query and a specific display table you can achieve basically the same\n\
  translation as above.\n\
  \n\
  echo \",! qk br{n fox\" | lou_translate --backward en-us-g2.ctb\n\
  \n\
  Do a backward translation with table en-us-g2.ctb.\n",
			stdout);
	printf("\n");
	printf("Report bugs to %s.\n", PACKAGE_BUGREPORT);

#ifdef PACKAGE_PACKAGER_BUG_REPORTS
	printf("Report %s bugs to: %s\n", PACKAGE_PACKAGER, PACKAGE_PACKAGER_BUG_REPORTS);
#endif
#ifdef PACKAGE_URL
	printf("%s home page: <%s>\n", PACKAGE_NAME, PACKAGE_URL);
#endif
}

int main(int argc, char **argv) {
	int optc;

	int forward_flag = 0;
	int backward_flag = 0;
	char *display_table = NULL;

	const struct option longopts[] = {
		{ "help", no_argument, NULL, 'h' },
		{ "version", no_argument, NULL, 'v' },
		{ "forward", no_argument, NULL, 'f' },
		{ "backward", no_argument, NULL, 'b' },
		{ "display-table", required_argument, NULL, 'd' },
		{ NULL, 0, NULL, 0 },
	};

	set_program_name(argv[0]);
	while ((optc = getopt_long(argc, argv, "hvfb", longopts, NULL)) != -1) {
		switch (optc) {
		/* --help and --version exit immediately, per GNU coding standards. */
		case 'v':
			version_etc(
					stdout, program_name, PACKAGE_NAME, VERSION, AUTHORS, (char *)NULL);
			exit(EXIT_SUCCESS);
			break;
		case 'h':
			print_help();
			exit(EXIT_SUCCESS);
			break;
		case 'f':
			forward_flag = 1;
			break;
		case 'b':
			backward_flag = 1;
			break;
		case 'd':
			display_table = optarg;
			break;
		default:
			fprintf(stderr, "Try `%s --help' for more information.\n", program_name);
			exit(EXIT_FAILURE);
			break;
		}
	}

	if (forward_flag && backward_flag) {
		fprintf(stderr, "%s: specify either -f or -b but not both\n", program_name);
		fprintf(stderr, "Try `%s --help' for more information.\n", program_name);
		exit(EXIT_FAILURE);
	}

	if (optind >= argc) {
		fprintf(stderr, "%s: no table specified\n", program_name);
		fprintf(stderr, "Try `%s --help' for more information.\n", program_name);
		exit(EXIT_FAILURE);
	}

	if (display_table && !lou_checkTable(display_table)) {
		lou_free();
		exit(EXIT_FAILURE);
	}

	char *tableOption;
	int validQuery;
	int queryHasColon;	// note that a query must always have a colon now, but we'll keep
						// some of this code for now because of
						// https://github.com/liblouis/liblouis/issues/1671
	{
		validQuery = 1;
		queryHasColon = 0;
		int len = 0;
		for (int i = optind; i < argc; i++) {
			int l = strlen(argv[i]);
			if (validQuery) {
				int hasColon = 0;
				for (int j = 0; j < l; j++) {
					if (argv[i][j] == ':') {
						if (j == 0 || j == l - 1 || hasColon)
							validQuery = 0;
						else
							hasColon = 1;
					} else if (!isValidChar(argv[i][j]))
						validQuery = 0;
				}
				if (hasColon)
					queryHasColon = 1;
				else
					validQuery = 0;
			}
			len += l;
			len++;
		}
		len--;
		tableOption = calloc((1 + len), sizeof(char));
		for (int i = optind; i < argc; i++) {
			if (i > optind) strcat(tableOption, " ");
			strcat(tableOption, argv[i]);
		}
	}

	char *table;
	int mode = 0;
	int exitValue = EXIT_FAILURE;
	{
		if (optind == argc - 1 && validQuery) {
			// could be both a query or a file list
			if (queryHasColon) {
				// first try query
				table = lou_findTable(tableOption);
				if (table != NULL && !display_table)
					mode |= dotsIO | ucBrl;
				else
					table = strdup(argv[optind]);
				if (!lou_checkTable(table)) goto failure;
			} else {
				// first try file list (note that this will currently never happen, but
				// see #1671)
				table = argv[optind];
				if (lou_checkTable(table))
					table = strdup(table);
				else {
					table = lou_findTable(tableOption);
					if (table == NULL || !lou_checkTable(table)) goto failure;
					if (!display_table) mode |= dotsIO | ucBrl;
				}
			}
		} else if (validQuery) {
			table = lou_findTable(tableOption);
			if (table == NULL || !lou_checkTable(table)) goto failure;
			if (!display_table) mode |= dotsIO | ucBrl;
		} else if (optind == argc - 1) {
			table = strdup(argv[optind]);
			if (!lou_checkTable(table)) goto failure;
		} else {
			fprintf(stderr, "%s: no valid table specified: %s\n", program_name,
					tableOption);
			fprintf(stderr, "Must be a query or table list\n");
			fprintf(stderr, "Try `%s --help' for more information.\n", program_name);
			free(tableOption);
			exit(EXIT_FAILURE);
		}
	}

	/* assume forward translation by default */
	translate_input(!backward_flag, table, display_table, mode, stdin);

success:
	exitValue = EXIT_SUCCESS;
failure:
	free(tableOption);
	free(table);
	lou_free();
	exit(exitValue);
}
