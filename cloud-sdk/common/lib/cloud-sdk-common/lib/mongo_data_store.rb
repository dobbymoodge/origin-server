require 'rubygems'
require 'mongo'

module Cloud::Sdk
  class MongoDataStore < DataStore
    @cdk_ds_provider = Cloud::Sdk::MongoDataStore
    DOT = "."
    DOT_SUBSTITUTE = "(ö)"  
 
    def self.provider=(provider_class)
      @cdk_ds_provider = provider_class
    end
    
    def self.instance
      @cdk_ds_provider.new
    end
    
    def find(obj_type, user_id, id)
      Rails.logger.debug "MongoDataStore.find(#{obj_type}, #{user_id}, #{id})\n\n"
      case obj_type
      when "CloudUser"
	MongoDataStore.get_user(user_id)
      when "Application"
	MongoDataStore.get_app(user_id, id)
      end
    end
    
    def find_all(obj_type, user_id=nil)
      Rails.logger.debug "MongoDataStore.find_all(#{obj_type}, #{user_id})\n\n"
      case obj_type
      when "CloudUser"
	MongoDataStore.get_users
      when "Application"
	MongoDataStore.get_user_apps(user_id)
      end
    end
    
    def save(obj_type, user_id, id, obj_bson)
      Rails.logger.debug "MongoDataStore.save(#{obj_type}, #{user_id}, #{id}, #{obj_bson})\n\n"
      case obj_type
      when "CloudUser"
	MongoDataStore.put_user(user_id, obj_bson)
      when "Application"
	MongoDataStore.put_app(user_id, id, obj_bson)
      end
    end
    
    def delete(obj_type, user_id, id=nil)
      Rails.logger.debug "MongoDataStore.delete(#{obj_type}, #{user_id}, #{id})\n\n"
      case obj_type
      when "CloudUser"
	MongoDataStore.delete_user(user_id)
      when "Application"
	MongoDataStore.delete_app(user_id, id)
      end
    end

    private

    def self.db
      con = Mongo::Connection.new(Rails.application.config[:datastore_mongo][:host], 
                                  Rails.application.config[:datastore_mongo][:port])
      con.db(Rails.application.config[:datastore_mongo][:db])
    end

    def self.collection
      MongoDataStore.db.collection(Rails.application.config[:datastore_mongo][:collection])
    end

    def self.get_user(user_id)
      mcursor = MongoDataStore.collection.find( "_id" => user_id )
      bson = mcursor.next
      return nil unless bson

      pkey = bson["_id"]
      bson.delete("_id")
      bson.delete("apps")
      { pkey => bson.to_json }
    end

    def self.get_users
      mcursor = MongoDataStore.collection.find()
      return [] unless mcursor

      ret = []
      mcursor.each do |bson|
        pkey = bson["_id"]
        bson.delete("_id")
        bson.delete("apps")
        ret.push({ pkey => bson.to_json })
      end
      ret
    end

    def self.get_app(user_id, id)
      select_fields = "apps." + id
      mcursor = MongoDataStore.collection.find({ "_id" => user_id }, :fields => [select_fields])
      bson = mcursor.next
      return nil unless (bson and bson["apps"])

      # Hack to overcome mongo limitation: Mongo key name can't have '.' char
      app_bson = bson["apps"][id]
      embedded_carts = {}
      app_bson["embedded"].each do |cart_name, cart_info|
        cart_name = cart_name.gsub(DOT_SUBSTITUTE, DOT)
        embedded_carts[cart_name] = cart_info
      end if app_bson and app_bson["embedded"]
      app_bson["embedded"] = embedded_carts if app_bson

      { id => app_bson.to_json }
    end
  
    def self.get_user_apps(user_id)
      mcursor = MongoDataStore.collection.find({ "_id" => user_id }, :fields => ["apps"] )
      bson = mcursor.next
      return [] unless (bson and bson["apps"])

      apps_bson = bson["apps"]
      ret = []
      apps_bson.each do |app_id, app_bson|
        ret.push({ app_id => app_bson.to_json })
      end
      ret
    end

    def self.put_user(user_id, user_bson)
      mcursor = MongoDataStore.collection.find( "_id" => user_id )
      bson = mcursor.next

      if bson
        apps = bson["apps"]
        user_bson["_id"] = user_id
        user_bson["apps"] = apps
        MongoDataStore.collection.update({ "_id" => user_id }, user_bson)
      else
        user_bson["_id"] = user_id
        MongoDataStore.collection.insert(user_bson)
      end
    end

    def self.put_app(user_id, id, app_bson)
      field = "apps." + id

      # Hack to overcome mongo limitation: Mongo key name can't have '.' char
      embedded_carts = {}
      app_bson["embedded"].each do |cart_name, cart_info|
        cart_name = cart_name.gsub(DOT, DOT_SUBSTITUTE)
        embedded_carts[cart_name] = cart_info
      end if app_bson and app_bson["embedded"]
      app_bson["embedded"] = embedded_carts if app_bson

      MongoDataStore.collection.update({ "_id" => user_id }, { "$set" => { field => app_bson }})
    end

    def self.delete_user(user_id)
      MongoDataStore.collection.remove({ "_id" => user_id })
    end

    def self.delete_app(user_id, id)
      field = "apps." + id
      MongoDataStore.collection.update({ "_id" => user_id }, { "$unset" => { field => 1 }})
    end

  end
end
