metadata    :name        => "Libra Management",
            :description => "Agent to manage Libra services",
            :author      => "Mike McGrath",
            :license     => "GPLv2",
            :version     => "0.1",
            :url         => "https://engineering.redhat.com/trac/Libra",
            :timeout     => 360


action "migrate", :description => "migrate a gear" do
    display :always

    input :uuid,
        :prompt         => "Gear uuid",
        :description    => "Gear uuid",
        :type           => :string,
        :validation     => '^[a-zA-Z0-9]+$',
        :optional       => false,
        :maxlength      => 32
        
    input :namespace,
        :prompt         => "Namespace",
        :description    => "Namespace",
        :type           => :string,
        :validation     => '^.+$',
        :optional       => false,
        :maxlength      => 32

    input :version,
        :prompt         => "Target Version",
        :description    => "Target version",
        :type           => :string,
        :validation     => '^.+$',
        :optional       => false,
        :maxlength      => 64

    output  :time,
            :description => "The time as a message",
            :display_as => "Time"

    output  :output,
            :description => "Output from script",
            :display_as => "Output"

    output :exitcode,
           :description => "Exit code",
           :display_as => "Exit Code"
end
