/*
 * Diamond example filter
 *
 * This code is licensed under a permissive license and is meant to be
 * copied and incorporated into other projects.
 *
 * Copyright (c) 2008, Carnegie Mellon University
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 *  * Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 *  * Redistributions in binary form must reproduce the above
 *    copyright notice, this list of conditions and the following
 *    disclaimer in the documentation and/or other materials provided
 *    with the distribution.
 *
 *  * Neither the name of the Carnegie Mellon University nor the names
 *    of its contributors may be used to endorse or promote products
 *    derived from this software without specific prior written
 *    permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 * COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
 * STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
 * OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#define _GNU_SOURCE
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <limits.h>

#include "lib_filter.h"


typedef struct {
  char *target_str;
} context_t;

// 2 functions for diamond filter interface
int f_init_string (int num_arg, const char * const *args,
		    int bloblen, const void *blob_data,
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
  const void *data;
  lf_ref_attr(ohandle, "", &len, &data);

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

// Declare the init and eval functions we want to use
LF_MAIN(f_init_string, f_eval_string)
