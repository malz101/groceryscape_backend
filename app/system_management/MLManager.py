# import all lib for ML
import numpy as np
class MLManager:

    def __init__(self, customerAccess, orderAccess, ratingAccess, cartAccess):
        self.customerAccess = customerAccess
        self.orderAccess = orderAccess
        self.ratingAccess = ratingAccess
        self.cartAccess = cartAccess

    def getRecommendGroceries(self, customerId):
        """ Uses a Pearson product-moment correlation coefficient matrix
            to determine the similarity among customers based on preferences
            specified by ratings then by the amount of items purchased over
            the lifetime of the account. """

        def organize(rawData, getRow, getCol, getData):
            """ Organizes the data into a 2D dictionary and returns the dictionary
                along with a list of all the unique keys that occur in the
                sub-dictionaries """

            dataDict = {}
            columns = set()
            for rd in rawData:
                # Organizes the data in a dictionary indexed by customerID
                try:
                    dataDict[getRow(rd)][getCol(rd)] = getData(rd)
                except KeyError:
                    dataDict[getRow(rd)] = {}
                    dataDict[getRow(rd)][getCol(rd)] = getData(rd)

                # List of all the items encountered
                columns.add(getCol(rd))
            return (dataDict, [i for i in columns])

        def genMatrix(id, rowIndexLst, colIndexLst, custDict, defaultVal):
            """ Converts a 2D dictionary into a 2D list """

            data = []
            cnt = 0
            for c in rowIndexLst:
                if (c == id):
                    custIndex = cnt

                data.append([])
                for iid in colIndexLst:
                    try:
                        data[cnt].append(custDict[c][iid])
                    except KeyError:
                        data[cnt].append(defaultVal)
                cnt += 1
            return (data, custIndex)

        def getMostSimilar(element, matrix, indexToIdMap):
            """ Uses Pearson product-moment correlation coefficient matrix
                to determine the most similar elements of a matrix """

            closest = []
            for i in range(len(matrix)):
                correlMatrix = np.corrcoef(element, matrix[i])
                correl = correlMatrix[0][1]
                if ((correl < 1) and (correl > 0.75)):
                    closest.append((indexToIdMap[i], correl))
            closest.sort(key=lambda x: x[1], reverse=True)
            closest = list(map(lambda x: x[0], closest))
            return closest

        custId = int(customerId)
        recommendCnt = 30

        # Find similar customers based on ratings provided
        ratings = self.ratingAccess.getAllRatings()
        ratingsDict, itemLst = organize(ratings, lambda d: d.cust_id, \
                                lambda d: d.item_id, lambda d: d.rating)
        similarCustomers = []
        if (custId in ratingsDict): # ie: if the customer has rated something in the past
            # Ratings range from 1 to 10. Ratings < 5 are thought to be
            # negative while ratings above 5 are thought to be positive
            # hence using a default value of 5 implies an average or
            # indifferent perception of an item
            custLst = list(ratingsDict.keys())
            ratingsLst, custIndex = genMatrix(custId, custLst, itemLst, ratingsDict, 5)
            similarCustomers = getMostSimilar(ratingsLst[custIndex], ratingsLst, custLst)

        # If similar customers were found, search for customers with similar
        # order history from that set of customers, otherwise compare all
        # customers to find customers that have a similar pattern of items
        # purchased over the lifetime of the account
        quantityDict = self.customerAccess.getTotalAmtPurchased(similarCustomers)
        if (custId in quantityDict): # ie: if the customer has ordered something in the past
            custLst = list(quantityDict.keys())

            # Generate list of items
            itemSet = set()
            for q in quantityDict.values():
                itemSet.update(q.keys())
            itemLst =  [c for c in itemSet]

            quantityLst, custIndex = genMatrix(custId, custLst, itemLst, quantityDict, 0)
            similarCustomers = getMostSimilar(quantityLst[custIndex], quantityLst, custLst)

        recommendedItems = set()
        cart = self.cartAccess.getAllCartItems(custId)
        if (type(cart) == list):
            cart = set(list(map(lambda i: i.item_id, cart)))
        else:
            cart = []

        # Extracts a list of items bought by similar customers that haven't
        # been bought by the current customer. Items in the customers cart
        # are also ignored
        for c in similarCustomers[:15]:
            for gid in quantityDict[c].keys():
                try:
                    if quantityDict[custId][gid]:
                        pass
                except KeyError:
                    if (not (gid in cart)):
                        recommendedItems.add(gid)

        # Pad the rest with items frequently bought together.
        if (len(recommendedItems) < recommendCnt):
            groceries = set(cart)
            if (custId in ratingsDict):
                # Finds all items that the customer has rated positively
                for g in ratingsDict[custId].keys():
                    if (ratingsDict[custId][g] > 5):
                        groceries.add(g)
            elif (custId in quantityDict):
                # Adds all items that the customer has ever bought
                groceries.update(quantityDict[custId].keys())

            pairFreq = self.getFreqBoughtWith(list(groceries))
            i = 0
            while ((len(recommendedItems) < recommendCnt) and (i < len(pairFreq))):
                recommendedItems.add(pairFreq[i][0])
                i += 1

        # Pad the list with the most purchased items
        if (len(recommendedItems) < recommendCnt):
            popularItems = self.getPopularItems()
            i = 0
            while ((len(recommendedItems) < recommendCnt) and (i < len(popularItems))):
                recommendedItems.add(popularItems[i][0])
                i += 1

        return [r for r in recommendedItems]


    def getFreqBoughtWith(self, gid):
        """ Accepts a groceryID or list of grocery IDs and returns a sorted
            list of pairs with the frequency of occurence """

        test = self.customerAccess.getOrders()[0]
        print('Test: ', test)
        print('Test: ', test.groceries)
        pairDict = self.orderAccess.getGroceryPairFreq(gid)
        pairFreq = []
        for g1, pairCnt in pairDict.items():
            for g2, freq in pairCnt.items():
                pairFreq.append((g1, g2, freq))
        pairFreq.sort(key=lambda p: p[2], reverse=True)

        return pairFreq


    def getPopularItems(self):
        """ Returns the top 30 most purchased items in the system """

        quantities = self.orderAccess.getTotalQuantityPurchased()
        quantityLst = list(quantities.items())
        quantityLst.sort(key=lambda q: q[1], reverse=True)
        return list(map(lambda q: q[0], quantityLst[:30]))
