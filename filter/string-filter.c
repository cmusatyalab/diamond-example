#define _GNU_SOURCE
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <limits.h>

#include "lib_filter.h"


typedef struct {
  char *target_str;
} context_t;

// 3 functions for diamond filter interface
int f_init_string (int num_arg, char **args,
		    int bloblen, void *blob_data,
		    const char *filter_name,
		    void **filter_args) {
  // check args
  if (num_arg < 1) {
    return -1;
  }

  // make space for callback structure
  context_t *ctx = (context_t *) malloc(sizeof(context_t));

  // args is:
  // 1. target_string: string to search for in each object

  // fill in
  ctx->target_str = strdup(args[0]);

  // ready?
  *filter_args = ctx;
  return 0;
}



int f_eval_string (lf_obj_handle_t ohandle, void *filter_args) {
  context_t *ctx = (context_t *) filter_args;
  const char *target_str = ctx->target_str;
  int result = 0;

  // slurp in the object
  size_t len;
  unsigned char *data;
  lf_next_block(ohandle, INT_MAX, &len, &data);

  char *source = malloc(len + 1);
  if (source == NULL) {
    return 0;
  }

  memcpy(source, data, len);
  source[len] = '\0';

  char *strstr_result = strstr(source, target_str);

  if (strstr_result != NULL) {
    // found, get index
    int index = strstr_result - source;

    // put into attribute
    char *index_str;
    asprintf(&index_str, "%d", index);
    lf_write_attr(ohandle, "string-index", strlen(index_str) + 1,
		  (unsigned char *) index_str);
    free(index_str);

    result = 1;
  }

  free(source);
  return result;
}



int f_fini_string (void *filter_args) {
  context_t *ctx = (context_t *) filter_args;

  free(ctx->target_str);

  free(ctx);
  return 0;
}
