#ifndef LINKED_LIST_H
#define LINKED_LIST_H

// Linked list node declaration
typedef struct LinkedListNode LinkedListNode;
struct LinkedListNode {
    LinkedListNode* next;
    void* data;
};

// Linked list declaration
typedef struct LinkedList LinkedList;
struct LinkedList {
    LinkedListNode* head;
    size_t length;
};

#endif
