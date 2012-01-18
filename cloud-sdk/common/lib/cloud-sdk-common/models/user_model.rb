module Cloud
  module Sdk
    class UserModel < Model
      
      def initialize()
        super()
      end
      
      def self.find(login, id)
        id_var = @primary_key || "uuid"        
        data = DataStore.instance.find(self.name,login,id)
        return nil unless data
        
        obj = self.new.from_json(data.values[0])
        obj.instance_variable_set("@#{id_var}", data.keys[0])
        obj.reset_state
        obj
      end
      
      def self.find_all(login)
        id_var = @primary_key || "uuid"        
        data_list = DataStore.instance.find_all(self.name,login)
        return [] unless data_list
        data_list.map! do |data|
          obj = self.new.from_json(data.values[0])
          obj.instance_variable_set("@#{id_var}", data.keys[0])
          obj.reset_state
          obj
        end
      end
      
      def delete(login)
        id_var = self.class.pk || "uuid"
        DataStore.instance.delete(self.class.name, login, instance_variable_get("@#{id_var}"))
      end
      
      def save(login)
        id_var = self.class.pk || "uuid"        
        @previously_changed = changes
        @changed_attributes.clear
        @new_record = false
        @persisted = true
        @deleted = false
        DataStore.instance.save(self.class.name, login, instance_variable_get("@#{id_var}"), self.attributes)
        self
      end
      
      protected

    end
  end
end
