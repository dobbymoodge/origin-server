def selinux_policy_name
  'openshift-hosted'
end

def ext_packages
  [ 'rhc-common', 'rhc-node', 'rhc-selinux' ]
end

def check_selinux_additional()
  verbose("checking selinux nodes")

  min_uid = 500
  max_uid = 16000
  min_node_ents = max_uid - min_uid + 5

  min_mcs_label = %x[oo-get-mcs-level #{min_uid}].strip
  max_mcs_label = %x[oo-get-mcs-level #{max_uid}].strip

  nodeset = %x[/usr/sbin/semanage node -l]

  combined_check=true
  setlen = nodeset.lines.to_a.length
  if setlen < min_node_ents
    do_fail("Not enough selinux nodes: #{setlen} (did rhc-ip-prep run?)")
    combined_check=false
  end

  if not ( min_mcs_label =~ /^s0\:c\d+\,c\d+$/ and min_mcs_label =~ /^s0\:c\d+\,c\d+$/ )
    do_fail("Was not able to get MCS labels for the min or max uids")
    combined_check=false
  end

  if combined_check
    setlen = nodeset.lines.select { |l|
      l.include?(min_mcs_label) or
      l.include?(max_mcs_label)
    }.length
    if setlen < 2
      do_fail("Selinux nodes do not include beginning and end of the range.")
    end
  end

end
