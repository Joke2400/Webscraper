    def activate_store_search(self):
        if not self.name_search_performed:
            self.name_search_performed = True
            
            if self.store_name is not None:
                for store in self.stores:
                    if self.store_name.lower() == store.lower():
                        
                        if self.store_href is not None:
                            if not check_key_value_consistency():
                                print("Saved store data key/value pair was not consistent with provided data")

                                if self.store_href != self.stores[store]:
                                    self.name_search_performed = False
                                    print("Provided store href was determined to be inconsistent with saved data, ensuring a search is performed with both hrefs...")
                                    
                                    search_url = {"URL" : prepare_search_string(URLS.STORE_SELECT_BASE_URL, self.stores[store]), "CALLBACK" : self.schedule_requests}
                                    self.stores[store] = self.store_href
                                    return search_url
                    
                        search_url = {"URL" : prepare_search_string(URLS.STORE_SELECT_BASE_URL, store["href"]), "CALLBACK" : self.schedule_requests}
                        return search_url
        else:
            print("Store search using locally stored name data has failed.")

        if not self.href_search_performed:
            self.href_search_performed = True
            
            if self.store_href is not None:
                if self.store_href in self.stores.values():
                    for href in self.stores.values():
                        if self.store_href.lower() == href.lower():
                            if self.store_name is not None:
                                if not ensure_key_value_consistency(self.stores, ("VALUE", self.store_href), self.store_name):
                                    print("Saved store data key/value pair was not consistent with provided data")
                                    self.delete_store_data() #Must pass args for exactly what is to be deleted!!!
                        
                            search_url = {"URL" : prepare_search_string(URLS.STORE_SELECT_BASE_URL, href.lower()), "CALLBACK" : self.schedule_requests}
                            return search_url
                
                else:
                    search_url = {"URL" : prepare_search_string(URLS.STORE_SELECT_BASE_URL, self.store_href), "CALLBACK" : self.schedule_requests}
                    return search_url

        else:
            print("Store search using locally stored href data has failed.")
                
        self.local_store_search_performed = True
        self.delete_store_data()#Must pass args for exactly what is to be deleted!!!
        print("Scraping website for the correct store using provided data...")
        search_url = self.query_website_for_store()
        return search_url
