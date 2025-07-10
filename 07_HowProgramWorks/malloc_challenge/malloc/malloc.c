//
// >>>> malloc challenge! <<<<
//
// Your task is to improve utilization and speed of the following malloc
// implementation.
// Initial implementation is the same as the one implemented in simple_malloc.c.
// For the detailed explanation, please refer to simple_malloc.c.

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 8 // binの数

//
// Interfaces to get memory pages from OS
//

void *mmap_from_system(size_t size);
void munmap_to_system(void *ptr, size_t size);

//
// Struct definitions
//

typedef struct my_metadata_t {
  size_t size;
  struct my_metadata_t *next;
} my_metadata_t;

typedef struct my_heap_t {
  my_metadata_t *free_head[N];
  my_metadata_t dummy;
} my_heap_t;

//
// Static variables (DO NOT ADD ANOTHER STATIC VARIABLES!)
//
my_heap_t my_heap;

//
// Helper functions (feel free to add/remove/edit!)
//

void my_add_to_free_list(my_metadata_t *metadata, int bin_index) {
  assert(!metadata->next);
  metadata->next = my_heap.free_head[bin_index];
  my_heap.free_head[bin_index] = metadata;
}

void my_remove_from_free_list(my_metadata_t *metadata, my_metadata_t *prev, int bin_index) {
  if (prev) {
    prev->next = metadata->next;
  } else {
    my_heap.free_head[bin_index] = metadata->next;
  }
  metadata->next = NULL;
}

// sizeが与えられたときに、それがどのビンに入るかを返す関数
int calculate_bin_index(size_t size){
  int bin_size_start[N] = {0,100,300,500,700,900,1000,1200};  // 各indexのbinの最小値が入っている配列
  for( int i = 0 ; i < N ; i++ ){
    if(size <= bin_size_start[i]){  // i番目のbinでは大きすぎるとき
      return i-1;
    }
  }
  return N-1; // 一番大きいときは、最後のbinに入ってもらう
}

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

// This is called at the beginning of each challenge.
void my_initialize() {
  for( int i = 0 ; i < N ; i++ ){
    my_heap.free_head[i] = &my_heap.dummy;
  }
  my_heap.dummy.size = 0;
  my_heap.dummy.next = NULL;
}

// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than
// mmap_from_system() / munmap_to_system().
void *my_malloc(size_t size) {
  if (size == 0){
    return NULL;
  }
  int bin_index = calculate_bin_index(size);  // sizeが確保できそうなbin_inexを探す
  my_metadata_t *metadata = my_heap.free_head[bin_index]; // そのbinの中から、確保するメモリを決める
  my_metadata_t *prev = NULL;

  // First-fit: Find the first free slot the object fits.
  // TODO: Update this logic to Best-fit!
  // while (metadata && metadata->size < size) { // sizeの入ることができるmetadataの場所を探すまでループ
  //   prev = metadata;
  //   metadata = metadata->next;
  // }

  // printf("%ld ",size); // 各要求サイズの出力を行って、binの範囲を考える
  
  // Best-fit
  my_metadata_t *best_metadata = NULL;
  my_metadata_t *best_prev = NULL;
  for( int i = bin_index ; i < N ; i ++ ){
    metadata = my_heap.free_head[i];
    prev = NULL;

    while (metadata) {
      if (size <= metadata->size){  // sizeよりも大きいmetadata->sizeが見つかった
        if ( best_metadata == NULL || metadata->size < best_metadata->size){ // 必要なサイズ < metadataのサイズ < 今のベストサイズ のとき
          best_metadata = metadata;
          best_prev = prev;
        }
      }
      prev = metadata;
      metadata = metadata->next;
    }
    if (best_metadata){ // 見つかったとき
      break;
    }
  }
  
  prev = best_prev;
  metadata = best_metadata;


  // now, metadata points to the first free slot
  // and prev is the previous entry.

  if (!metadata) {  // metadataがなければ新しいメモリ領域を要求する
    // There was no free slot available. We need to request a new memory region
    // from the system by calling mmap_from_system().
    //
    //     | metadata | free slot |
    //     ^
    //     metadata
    //     <---------------------->
    //            buffer_size
    size_t buffer_size = 4096;
    my_metadata_t *metadata = (my_metadata_t *)mmap_from_system(buffer_size);
    metadata->size = buffer_size - sizeof(my_metadata_t);
    metadata->next = NULL;
    // Add the memory region to the free list.
    my_add_to_free_list(metadata,calculate_bin_index(metadata->size));
    // Now, try my_malloc() again. This should succeed.
    return my_malloc(size);
  }

  // |ptr| is the beginning of the allocated object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  void *ptr = metadata + 1;
  size_t remaining_size = metadata->size - size;
  // Remove the free slot from the free list.
  my_remove_from_free_list(metadata, prev, calculate_bin_index(metadata->size));  //

  if (remaining_size > sizeof(my_metadata_t)) {
    // Shrink the metadata for the allocated object
    // to separate the rest of the region corresponding to remaining_size.
    // If the remaining_size is not large enough to make a new metadata,
    // this code path will not be taken and the region will be managed
    // as a part of the allocated object.
    metadata->size = size;
    // Create a new metadata for the remaining free slot.
    //
    // ... | metadata | object | metadata | free slot | ...
    //     ^          ^        ^
    //     metadata   ptr      new_metadata
    //                 <------><---------------------->
    //                   size       remaining size
    my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
    new_metadata->size = remaining_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    // Add the remaining free slot to the free list.
    my_add_to_free_list(new_metadata,calculate_bin_index(new_metadata->size));
  }
  return ptr;
}

// This is called every time an object is freed.  You are not allowed to
// use any library functions other than mmap_from_system / munmap_to_system.
void my_free(void *ptr) {
  // Look up the metadata. The metadata is placed just prior to the object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;

  // 左側と結合するとき
  for (int i = 0; i < N ; i++ ){
    my_metadata_t *cur = my_heap.free_head[i];
    my_metadata_t *prev = NULL;
    while (cur){  // 現在のビンを全て探索する
      
      if((cur+1 + cur->size)==metadata){
        //  | free_metadata | free | metadata | object | ...
        //  ^                      ^          ^         
        //  cur       cur+1+size = metadata   ptr
        // cur + 1 + cur->size == metadataだったとき、左側結合をする
        my_remove_from_free_list(cur,prev,calculate_bin_index(cur->size)); // そのリストをいったん削除
        cur->size += sizeof(my_metadata_t) + metadata->size; // 次のmetadataのサイズとそのsizeの分を足しいれる
        my_add_to_free_list(cur,calculate_bin_index(cur->size));
        return;
      }
      prev = cur;
      cur = cur->next;
    }
  }
  // Add the free slot to the free list.
  my_add_to_free_list(metadata,calculate_bin_index(metadata->size));
}

// This is called at the end of each challenge.
void my_finalize() {
  // Nothing is here for now.
  // feel free to add something if you want!
}

void test() {
  // Implement here!
  assert(1 == 1); /* 1 is 1. That's always true! (You can remove this.) */
}
