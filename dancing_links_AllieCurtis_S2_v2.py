#!/usr/bin/python3

import unittest

##### Doubly-Linked List: DO NOT MODIFY #####
class Node():
    """Node: An element in the linked list

    :ivar prevPtr: pointer to the node on the left
    :ivar nextPtr: pointer to the node on the right
    :ivar abovePtr: pointer to the upward node
    :ivar belowPtr: pointer to the downward node"""

    def __init__(self, name = None, header = None,  prevPtr = None, nextPtr = None, abovePtr = None, belowPtr = None):
        """Create a new node object

        :param name: the row number of the node
        :type name: str
        :param header: a pointer to that element's column header
        :type header: ListHeader
        :param prevPtr: a pointer to the left node or None
        :type prevPtr: Node
        :param nextPtr: a pointer to the right node or None
        :type nextPtr: Node
        :param abovePtr: a pointer to the upper node or None
        :type abovePtr: Node
        :param belowPtr: a pointer to the below node or None
        :type belowPtr: Node"""

        self.name = name
        self.header = header
        self.prevPtr = prevPtr
        self.nextPtr = nextPtr
        self.abovePtr = abovePtr
        self.belowPtr = belowPtr

    def __str__(self):
        return str(self.name)

class ColumnObject(Node):
    """ColumnObject: 

    :ivar size: 
    :type size: int"""

    def __init__(self, name = None, header = None, prevPtr = None, nextPtr = None, abovePtr = None, belowPtr = None, size = 0):
        """Create a new ColumnObject object - inherits from Node in all fields excluding the below:
        
        :param size:
        :type size: int"""

        super().__init__(name, header, prevPtr, nextPtr, abovePtr, belowPtr)
        self.size = size
        self.setHeader()

    def setHeader(self):
        """Sets the header object's header pointer to itself"""

        self.header = self

class LinkedList():
    """LinkedList: """

    def __init__(self, name = None):
        """Create new LinkedList object
        
        :var head:
        :type head: Node
        :var tail: 
        :type tail: Node
        :var length: 
        :type length: int"""
        self.name = name
        self.head = None
        self.tail = None
        self.length = 0

    def isEmpty(self):
        """Checks for an empty list
        
        :return: whether the list is empty or not
        :rtype: boolean"""

        return self.head is None

    def insert(self, node):
        """Insert node into list - always inserts at tail
        
        :param node: a node reference
        :type node: Node
        :return: if node is not initialized
        :rtype: None"""

        if node is None:
            return
        if self.isEmpty():
            self.head = node
            self.tail = node
            node.nextPtr = node
            node.prevPtr = node
        else:
            node.prevPtr = self.tail
            node.nextPtr = self.head
            self.tail.nextPtr = node
            self.head.prevPtr = node
            self.tail = node
        if self.isNotRoot(node):
            self.length += 1

    def delete(self, node):
        """Delete node from list
        
        :param node: a node reference
        :type node: Node
        :return: if the node is not initialized or if the list is empty
        :rtype: None"""

        if node is None or self.isEmpty():
            return
        if self.length == 1 and self.isNotRoot(self.head):
                self.head = None
                self.tail = None
        else:
            node.prevPtr.nextPtr = node.nextPtr
            node.nextPtr.prevPtr = node.prevPtr
            if node is self.head:
                self.head = node.nextPtr
            if node is self.tail:
                self.tail = node.prevPtr
        self.length -= 1

    def isNotRoot(self, node):
        """"""
        
        return node.name is not "root"

    def restore(self, node):
        """Restore node from list
        
        :param node:
        :type node: Node
        :return: if node is not in the list
        :rtype: None"""

        if node is None:
            return
        node.prevPtr.nextPtr = node
        node.nextPtr.prevPtr = node
        self.length += 1

    def search(self, headerName, searchNode = None):
        """Search for a certain node in the list and return it
        
        :param nodeName: the name of a node reference
        :type nodeName: str
        :param searchNode: the node to check against - set to self.head in first pass
        :type searchNode: Node
        :return: the specified node object if found, None if not found
        :rtype: Node"""

        if searchNode is self.head:
            return
        if not searchNode:
            searchNode = self.head
        if searchNode.header.name == headerName:
            return searchNode
        return self.search(headerName, searchNode.nextPtr)

    def __str__(self):
        """Returns a string representation of the list"""

        output = " " + str(self.head.name)
        nextElement = self.head.nextPtr
        while nextElement is not self.head:
            output += (" -> {}".format(nextElement.name) )
            nextElement = nextElement.nextPtr
        return output

class RowsList(LinkedList):
    """"""

    def __init__(self, name = None):
        """"""
        super().__init__()

    def search(self, index, searchNode = None):
        """"""

        if searchNode is self.head:
            return
        if not searchNode:
            searchNode = self.head
        if searchNode.name == index:
            return searchNode
        return self.search(index, searchNode.nextPtr)

class ColumnList(LinkedList):
    """ColumnList: 
    
    :ivar header:
    :type header: ColumnObject"""

    def __init__(self, header = None):
        """Create a new ColumnList object - inherits from LinkedList in all fields excluding the below:
        
        :param header: 
        :type header: ColumnObject"""

        super().__init__()
        self.header = header
        self.name =  header.name
        self.insert(header)

    def insert(self, node):
        """Insert node into the list - always inserts at the tail
        
        :param node: a node reference
        :type node: ColumnObject/Node"""

        if self.isEmpty():
            self.head = node
            self.tail = node
            node.belowPtr = node
            node.abovePtr = node
        else:
            node.abovePtr = self.tail
            node.belowPtr = self.head
            self.tail.belowPtr = node
            self.head.abovePtr = node
            self.tail = node
            self.length += 1
        self.updateHeaderSize()

    def delete(self, node):
        """Delete node from list - will not delete the column header
        
        :param node: a node reference
        :type node: Node"""

        if node is None or node is self.head:
            return
        node.belowPtr.abovePtr = node.abovePtr
        node.abovePtr.belowPtr = node.belowPtr
        if node is self.tail:
            self.tail = node.abovePtr
        self.length -= 1
        self.updateHeaderSize()

    def restore(self, node):
        """Restore node from list - cannot restore the head from an empty list
        
        :param node:
        :type node: Node
        :return: None if node is not in the list
        :rtype: None"""

        if node is None or node is self.head:
            return
        node.abovePtr.belowPtr = node
        node.belowPtr.abovePtr = node
        self.length += 1
        self.updateHeaderSize()

    def search(self, nodeName, searchNode = None):
        """Search for a certain node in the list and return it
        
        :param nodeName: the name of a node reference
        :type nodeName: int
        :param searchNode: the node to check against - set to self.head in first pass
        :type searchNode: Node
        :return: the specified node object if found, None if not found
        :rtype: Node"""

        if searchNode is self.head:
            return
        if not searchNode:
            searchNode = self.head
        if searchNode.name == nodeName:
            return searchNode
        return self.search(nodeName, searchNode.belowPtr)

    def updateHeaderSize(self):
        """Sets the header's size to the length of the list - used to prevent repetition"""
        
        self.header.size = self.length

    def __str__(self):
        """Returns a string representation of the list"""

        output = " " + str(self.head.name)
        nextElement = self.head.belowPtr
        while nextElement is not self.head:
            output += "\n v\n"
            output += (" {}".format(nextElement.name) )
            nextElement = nextElement.belowPtr
        return output

####### List Builder: DO NOT MODIFY #######
class ListBuilder():
    """"""

    def __init__(self, matrix):
        """"""

        self.matrix = matrix
        self.numOfRows = len(self.matrix)
        if self.checkRows():
            self.numOfColumns = len(self.matrix[0])
            if self.checkColumns():
                self.headers = self.createHeaders()
                self.nodes = self.createNodes()
                self.rowsList = self.createRowsList()
                self.columnsList = self.createColumnsList()

    def checkRows(self):
        """"""
        if self.numOfRows == 0:
            return False
        return True

    def checkColumns(self):
        """"""
        if self.numOfColumns > 26:
            print("ListBuilder cannot handle more than 26 columns - it will run out of names!")
            return False
        return True

    def createHeaders(self):
        """"""

        headers = []
        names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        for i in range(0, self.numOfColumns):
            header = ColumnObject(names[i])
            headers.append(header)
        return headers

    def createNodes(self):
        """"""

        nodes = []
        for i in range(0, self.numOfRows):
            for j in range(0, self.numOfColumns):
                if self.matrix[i][j] == 1:
                    name = i
                    header = self.headers[j]
                    node = Node(name, header)
                    nodes.append(node)
        return nodes

    def createRowsList(self):
        """"""

        rowsList = RowsList()
        for i in range(0, self.numOfRows):
            row = LinkedList(i)
            for node in self.nodes:
                if node.name == i:
                    row.insert(node)
            rowsList.insert(row)
        return rowsList

    def createColumnsList(self):
        """"""

        root = ColumnObject("root")
        columnsList = RowsList("root")
        columnsList.insert(root)
        for i in range(0, self.numOfColumns):
            header = self.headers[i]
            column = ColumnList(header)
            for node in self.nodes:
                if node.header == header:
                    column.insert(node)
            columnsList.insert(column)
        return columnsList

##### Dancing Links: Production Code #####
class DancingLinks():
    """"""

    def __init__(self, matrix):
        self.matrix = matrix
        self.lists = ListBuilder(self.matrix)
        self.partialSolution = [None]*self.lists.numOfRows
        self.coveredColumns = []
        self.coveredRows = []

    def solve(self, solution):
        i = 0
        for i < self.lists.numOfColumns:
            if self.columnsAreEmpty():
                return self.terminateSuccessfully(solution)
            c = self.chooseColumn()
            r = self.chooseRow(c)
            solution.append(r.name)
            self.coverColumn(c)
            self.coverRow(r)
            return self.solve(solution)
            i++

    def columnsAreEmpty(self):
        """"""

        return self.lists.columnsList.length == 0

    def chooseColumn(self):
        smallest = self.lists.numOfRows
        c = None
        for header in self.lists.headers:
            column = self.lists.columnsList.search(header.name)
            if column:
                if column.header.size > 0 and column.header.size < smallest:
                    smallest = column.header.size
                    c = column
        if c:
            self.coveredColumns.append(c)
            return c
        else:
            self.restoreRow()

    def chooseRow(self, c):
        """"""

        r = None
        for i in range(0, self.lists.numOfRows):
            row = self.lists.rowsList.search(i)
            if row:
                selection = row.search(c.header.name)
                if selection:
                    r = row
                    break
        if r:
            self.coveredRows.append(r)
            return r
        else:
            self.restoreColumn()

    def coverColumn(self, c):
        """"""

        self.lists.columnsList.delete(c)
        self.lists.headers.remove(c.header)
        for i in range(0, self.lists.numOfRows):
            row = self.lists.rowsList.search(i)
            for header in self.lists.headers:
                if row:
                    node = row.search(c.header.name)
                    if node:
                        row.delete(node)

    def coverRow(self, r):
        """"""

        for header in self.lists.headers:
            if r.search(header.name):
                header = r.search(header.name).header.name
                if header in self.lists.headers:
                    self.lists.headers.remove(header)
                column = self.lists.columnsList.search(header)
                self.lists.columnsList.delete(column)
        self.lists.rowsList.delete(r)

    def restoreColumn(self):
        """"""
        
        print("Column shit!")
        #print(self.coveredColumns.pop().name)

    def restoreRow(self):
        """"""
        r = self.coveredRows[-1]
        self.lists.rowsList.restore(r)
        
        
        #for i in range(0, c.header.size):
        #    if c.search(i):
        #        print(c.search(i).name)
        #print(self.coveredRows.pop().name)

    def terminateSuccessfully(self, solution):
        """"""
        
        return solution

"""    def coverNodes(self, c):
        """"""

        i = 0
        while(i < self.lists.numOfRows):
            row = self.lists.rowsList[i]
            node = row.search(c.header.name)
            if node:
                row.delete(node)
                self.coveredNodes.append(node)
            if row.isEmpty():
                self.lists.rowsList.remove(row)
                self.lists.numOfRows -= 1
            i += 1

    def restoreRow(self):
        """"""

        if not self.partialSolution:
            return self.terminateUnsuccessfully()
        r = self.partialSolution.pop()
        self.lists.rowsList.append(r)

    def restoreColumn(self):
        """"""

        if not self.coveredColumns:
            return self.terminateUnsuccessfully()
        c = self.coveredColumns.pop()
        self.lists.columnsList.append(c)
        self.lists.headersList.insert(c.header)

    def restoreNodes(self, c):
        """"""

        print(c)

    def terminateSuccessfully(self, solution):
        for s in self.partialSolution:
            if s != None:
                solution.append(s)
        return solution

    def terminateUnsuccessfully(self):
        return None"""

####### Test Cases: DO NOT MODIFY #######
class DancingLinks_UnitTest(unittest.TestCase):

    def setUp(self):
        self.list = LinkedList()
        self.header = ColumnObject(None)
        self.columnList = ColumnList(self.header)
        self.A = [[1, 0, 1],
                  [0, 0, 1],
                  [1, 1, 0]]
        self.B = [[1, 0, 0, 1],
                  [0, 1, 1, 0],
                  [0, 0, 1, 1],
                  [0, 0, 0, 1]]
        self.C = [[1, 0, 1, 0],
                  [0, 0, 1, 0],
                  [1, 1, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 0, 1]]
        self.D = [[1, 0, 1],
                  [0, 0, 1],
                  [0, 1, 0]]

### Doubly-Linked List ###
    def test_node_init_1(self):
        """Node creates some object"""
        node = Node()
        self.assertIsNotNone( node )

    def test_node_init_2(self):
        """Node works with parameters"""
        node1 = Node()
        node2 = Node(None, None, node1)
        self.assertEqual( node2.prevPtr, node1 )

    def test_column_object_init(self):
        header = ColumnObject("A")
        self.assertEqual( header.header, header )

    def test_linked_list_init(self):
        """LinkedList creates some object"""
        self.assertIsNotNone( self.list )

    def test_linked_list_is_empty(self):
        self.assertTrue( self.list.isEmpty() )

    def test_linked_list_length(self):
        """Empty LinkedList returns length of 0"""
        self.assertEqual( self.list.length, 0 )

    def test_linked_list_insert_1(self):
        """Length updates with insertion of node"""
        node = Node()
        self.list.insert(node)
        self.assertEqual( self.list.length, 1 )

    def test_linked_list_insert_2(self):
        """Length updates with insertion of two nodes"""
        node1 = Node()
        node2 = Node()
        self.list.insert(node1)
        self.list.insert(node2)
        self.assertEqual( self.list.length, 2 )

    def test_linked_list_insert_5(self):
        """If only one node, next pointer is to itself"""
        node = Node()
        self.list.insert(node)
        self.assertEqual( node.nextPtr, node )

    def test_linked_list_insert_7(self):
        """Testing pointers with two nodes, both next and previous should point to each other
        Will be tested in this and the next 3 tests"""
        node1 = Node()
        node2 = Node()
        self.list.insert(node1)
        self.list.insert(node2)
        self.assertEqual( node1.nextPtr, node2 )

    def test_linked_list_insert_8(self):
        node1 = Node()
        node2 = Node()
        self.list.insert(node1)
        self.list.insert(node2)
        self.assertEqual( node1.prevPtr, node2 )

    def test_linked_list_insert_9(self):
        node1 = Node()
        node2 = Node()
        self.list.insert(node1)
        self.list.insert(node2)
        self.assertEqual( node2.prevPtr, node1 )

    def test_linked_list_insert_10(self):
        node1 = Node()
        node2 = Node()
        self.list.insert(node1)
        self.list.insert(node2)
        self.assertEqual( node2.nextPtr, node1 )

    def test_linked_list_delete_1(self):
        """Delete empty node"""
        node = None
        self.assertIsNone( self.list.delete(node) )

    def test_linked_list_delete_2(self):
        """Delete from empty list"""
        node = Node()
        self.assertIsNone( self.list.delete(node) )

    def test_linked_list_delete_3(self):
        """Length is reduced to 0"""
        node = Node()
        self.list.insert(node)
        self.list.delete(node)
        self.assertEqual( self.list.length, 0 )

    def test_linked_list_delete_4(self):
        """Pointer is updated in case of 2 nodes"""
        node1 = Node()
        node2 = Node()
        self.list.insert(node1)
        self.list.insert(node2)
        self.list.delete(node1)
        self.assertEqual( node2.nextPtr, node2 )

    def test_linked_list_delete_5(self):
        """Pointer is updated in case of 3 nodes"""
        node1 = Node()
        node2 = Node()
        node3 = Node()
        self.list.insert(node1)
        self.list.insert(node2)
        self.list.insert(node3)
        self.list.delete(node2)
        self.assertEqual( node1.nextPtr, node3 )

    def test_linked_list_restore_1(self):
        """Restore node from 2 node list"""
        node1 = Node()
        node2 = Node()
        self.list.insert(node1)
        self.list.insert(node2)
        self.list.delete(node1)
        self.list.restore(node1)
        self.assertEqual( node2.prevPtr, node1 )

    def test_linked_list_restore_2(self):
        """Restore node from 3 node list"""
        node1 = Node()
        node2 = Node()
        node3 = Node()
        self.list.insert(node1)
        self.list.insert(node2)
        self.list.insert(node3)
        self.list.delete(node2)
        self.list.restore(node2)
        self.assertEqual( node1.nextPtr, node2 )

    def test_linked_list_search_1(self):
        """"""
        header = ColumnObject("A")
        node1 = Node(1, header)
        self.assertIsNone( self.list.search("A") )

    def test_linked_list_search_2(self):
        """"""
        header1 = ColumnObject("A")
        node1 = Node(1, header1)
        header2 = ColumnObject("B")
        node2 = Node(2, header2)
        self.list.insert(node1)
        self.list.insert(node2)
        self.assertEqual( self.list.search("B"), node2 )

    def test_column_list_init(self):
        """"""
        self.assertEqual( self.columnList.head, self.header )

    def test_column_list_is_empty(self):
        self.assertFalse( self.columnList.isEmpty() )

    def test_column_list_length(self):
        """"""
        self.assertEqual( self.columnList.length, 0 )

    def test_column_list_insert_1(self):
        """"""
        node = Node(None, self.header)
        self.columnList.insert(node)
        self.assertEqual( self.columnList.length, 1 )

    def test_column_list_insert_2(self):
        """"""
        node = Node(None, self.header)
        self.columnList.insert(node)
        self.assertEqual( node.belowPtr, self.header )

    def test_column_list_insert_3(self):
        """"""
        node = Node(None, self.header)
        self.columnList.insert(node)
        self.assertEqual( self.columnList.tail, node )

    def test_column_list_insert_4(self):
        """"""
        node1 = Node(1, self.header)
        node2 = Node(2, self.header)
        self.columnList.insert(node1)
        self.columnList.insert(node2)
        self.assertEqual( node1.belowPtr, node2 )

    def test_column_list_insert_5(self):
        """"""
        node1 = Node(1, self.header)
        node2 = Node(2, self.header)
        self.columnList.insert(node1)
        self.columnList.insert(node2)
        self.assertEqual( node2.abovePtr, node1 )

    def test_column_list_header_size_1(self):
        """"""
        self.assertEqual( self.header.size, 0 )

    def test_column_list_header_size_2(self):
        """"""
        node = Node(None, self.header)
        self.columnList.insert(node)
        self.assertEqual( self.header.size, 1 )

    def test_column_list_delete_1(self):
        """"""
        node = Node(None, self.header)
        self.columnList.insert(node)
        self.columnList.delete(node)
        self.assertEqual( self.columnList.length, 0 )

    def test_column_list_delete_2(self):
        """"""
        node = Node(None, self.header)
        self.columnList.insert(node)
        self.columnList.delete(node)
        self.assertEqual( self.header.belowPtr, self.header )

    def test_column_list_delete_3(self):
        """"""
        node1 = Node("1", self.header)
        node2 = Node("2", self.header)
        node3 = Node("3", self.header)
        self.columnList.insert(node1)
        self.columnList.insert(node2)
        self.columnList.insert(node3)
        self.columnList.delete(node2)
        self.assertEqual( node1.belowPtr, node3 )

    def test_column_list_restore_1(self):
        """"""
        node = Node("1", self.header)
        self.columnList.insert(node)
        self.columnList.delete(node)
        self.columnList.restore(node)
        self.assertEqual( self.header.belowPtr, node )

    def test_column_list_restore_2(self):
        """"""
        node1 = Node("1", self.header)
        node2 = Node("2", self.header)
        self.columnList.insert(node1)
        self.columnList.insert(node2)
        self.columnList.delete(node1)
        self.columnList.restore(node1)
        self.assertEqual( node2.abovePtr, node1 )

    def test_column_list_search_1(self):
        """"""
        node1 = Node("1", self.header)
        node2 = Node("2", self.header)
        self.columnList.insert(node1)
        self.assertIsNone( self.columnList.search("2") )

    def test_column_list_search_2(self):
        """"""
        node1 = Node("1", self.header)
        node2 = Node("2", self.header)
        self.columnList.insert(node1)
        self.columnList.insert(node2)
        self.assertEqual( self.columnList.search("2"), node2 )


### ListBuilder ###
    def test_list_builder_init_1(self):
        """"""
        builder = ListBuilder([])
        self.assertEqual( builder.numOfRows, 0 )

    def test_list_builder_init_2(self):
        """"""
        builder = ListBuilder([[]])
        self.assertEqual( builder.numOfColumns, 0 )

    def test_list_builder_init_3(self):
        """"""
        builder = ListBuilder(self.A)
        self.assertEqual( builder.numOfColumns, 3 )

    def test_list_builder_init_4(self):
        """"""
        builder = ListBuilder(self.A)
        self.assertEqual( builder.numOfRows, 3 )

    def test_list_builder_create_headers_1(self):
        """"""
        builder = ListBuilder(self.A)
        self.assertEqual( builder.columnsList.length, 3 )

    def test_list_builder_create_headers_2(self):
        """"""
        builder = ListBuilder(self.A)
        self.assertEqual( builder.columnsList.search("B").name, "B" )

    def test_list_builder_create_rows_1(self):
        """"""
        builder = ListBuilder(self.A)
        self.assertEqual( builder.rowsList.length, 3 )

    def test_list_builder_create_rows_2(self):
        """"""
        builder = ListBuilder(self.A)
        self.assertEqual( builder.rowsList.search(0).search("A").name, 0)

    def test_list_builder_create_rows_3(self):
        """"""
        builder = ListBuilder(self.A)
        target = builder.rowsList.search(0).search("C")
        self.assertEqual( builder.rowsList.search(0).search("A").nextPtr, target )

    def test_list_builder_create_rows_4(self):
        """"""
        builder = ListBuilder(self.A)
        target = builder.rowsList.search(2).search("B")
        self.assertEqual( builder.rowsList.search(2).search("A").prevPtr, target )

    def test_list_builder_create_columns_1(self):
        """"""
        builder = ListBuilder(self.A)
        self.assertEqual( builder.columnsList.length, 3 )

    def test_list_builder_create_columns_2(self):
        """"""
        builder = ListBuilder(self.A)
        self.assertEqual( builder.columnsList.search("A").length, 2 )

    def test_list_builder_create_columns_3(self):
        """"""
        builder = ListBuilder(self.A)
        column = builder.columnsList.search("A")
        target = column.search(2)
        self.assertEqual( builder.columnsList.search("A").search(0).belowPtr, target)

    def test_list_builder_create_columns_4(self):
        """"""
        builder = ListBuilder(self.A)
        target = builder.columnsList.search("C").search(0).header
        self.assertEqual( builder.columnsList.search("C").search(1).belowPtr, target)

    def test_list_builder_final_connection_1(self):
        """"""
        builder = ListBuilder(self.A)
        target = builder.columnsList.search("C").search(0)
        self.assertEqual( builder.rowsList.search(0).search("A").nextPtr, target )

    def test_list_builder_final_connection_2(self):
        """"""
        builder = ListBuilder(self.A)
        target = builder.columnsList.search("B").search(2)
        self.assertEqual( builder.rowsList.search(2).search("A").prevPtr, target )

### Dancing Links ###
    def test_dancing_links_init_1(self):
        """"""
        links = DancingLinks(self.A)
        self.assertEqual( links.lists.numOfColumns, 3 )

    def test_dancing_links_init_2(self):
        """"""
        links = DancingLinks(self.B)
        self.assertEqual( links.lists.numOfRows, 4 )

    def test_dancing_links_init_3(self):
        """"""
        links = DancingLinks(self.A)
        self.assertEqual( links.lists.columnsList.search("A").header.size, 2 )

    def test_dancing_links_columns_empty(self):
        """"""
        links = DancingLinks(self.A)
        headers = links.lists.columnsList
        headers.delete(headers.search("A"))
        headers.delete(headers.search("B"))
        headers.delete(headers.search("C"))
        self.assertTrue( links.columnsAreEmpty() )

    def test_dancing_links_choose_column_1(self):
        """"""
        links = DancingLinks(self.A)
        c = links.chooseColumn()
        self.assertEqual( c, links.lists.columnsList.search("B") )

    def test_dancing_links_choose_column_2(self):
        """"""
        links = DancingLinks(self.B)
        c = links.chooseColumn()
        self.assertEqual( c, links.lists.columnsList.search("A") )

    def test_dancing_links_choose_row_1(self):
        """"""
        links = DancingLinks(self.A)
        c = links.chooseColumn()
        r = links.chooseRow(c)
        self.assertEqual( r, links.lists.rowsList.search(2) )

    def test_dancing_links_choose_row_2(self):
        """"""
        links = DancingLinks(self.B)
        c = links.chooseColumn()
        r = links.chooseRow(c)
        self.assertEqual( r, links.lists.rowsList.search(0) )

    def test_dancing_links_cover_column_1(self):
        """"""
        links = DancingLinks(self.A)
        c =  links.chooseColumn()
        links.coverColumn(c)
        self.assertIsNone( links.lists.columnsList.search("B") )

    def test_dancing_links_cover_column_2(self):
        """"""
        links = DancingLinks(self.B)
        c = links.chooseColumn()
        links.coverColumn(c)
        self.assertIsNone( links.lists.columnsList.search("A") )

    def test_dancing_links_cover_row_1(self):
        """"""
        links = DancingLinks(self.A)
        c = links.chooseColumn()
        r = links.chooseRow(c)
        links.coverRow(r)
        self.assertEqual( links.lists.columnsList.search("C").header.belowPtr.name, 0 )

    def test_dancing_links_cover_row_2(self):
        """"""
        links = DancingLinks(self.B)
        c = links.chooseColumn()
        r = links.chooseRow(c)
        links.coverRow(r)

    def test_dancing_links_restore_column_1(self):
        """"""
        links = DancingLinks(self.C)
        c1 = links.chooseColumn()
        self.assertEqual( c1, links.lists.columnsList.search("D") )
        r1 = links.chooseRow(c1)
        self.assertEqual( r1, links.lists.rowsList.search(4) )
        links.coverColumn(c1)
        self.assertIsNone( links.lists.columnsList.search("D") )
        self.assertTrue( c1.header not in links.lists.headers )
        links.coverRow(r1)
        self.assertIsNone( links.lists.rowsList.search(4) )
        c2 = links.chooseColumn()
        self.assertEqual( c2, links.lists.columnsList.search("A") )
        r2 = links.chooseRow(c2)
        self.assertEqual( r2, links.lists.rowsList.search(0) )
        links.coverColumn(c2)
        self.assertIsNone( links.lists.columnsList.search("A") )
        links.coverRow(r2)
        self.assertIsNone( links.lists.rowsList.search(0) )
        self.assertIsNone( links.lists.columnsList.search("C") )
        c3 = links.chooseColumn()
        self.assertEqual( c3, links.lists.columnsList.search("B") )
        r3 = links.chooseRow(c3)
        self.assertEqual( r3, links.lists.rowsList.search(2) )
        links.coverColumn(c3)
        self.assertIsNone( links.lists.columnsList.search("B") )
        links.coverRow(r3)
        self.assertIsNone( links.lists.rowsList.search(2) )
        c4 = links.chooseColumn()
        

    def test_dancing_links_solve_1(self):
        """"""
        links = DancingLinks(self.D)
        self.assertEqual( links.solve([]), [0, 2] )

    def test_dancing_links_solve_2(self):
        """"""
        links = DancingLinks(self.B)
        self.assertEqual( links.solve([]), [0, 1] )





def main():
    unittest.main()

if __name__ == "__main__":
    main()