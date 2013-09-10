##
# @api model
# Represents an autogenerated SSH key used by a component in the application to access other application gears.
# @see Application#process_commands
class ApplicationSshKey < SshKey
  include Mongoid::Document
  field :component_id, type: Moped::BSON::ObjectId
  embedded_in :application, class_name: Application.name
end