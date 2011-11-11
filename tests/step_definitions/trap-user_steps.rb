require 'pty'

Given /^the user has (no|\d+) tail process(es)? running( in (\d+) seconds)?$/ do |expect, ignore1, ignore2, timeout|
  # convert to integer
  expect = (expect == "no" ? 0 : expect.to_i)
  timeout = timeout ? timeout.to_i : 0
  sleep timeout
  pcount = num_procs @app.uid, "tail"

  if pcount != expect
    raise Cucumber::Pending.new "failed given: expected #{expect}, actual #{pcount}" 
  end
end

Given /a running SSH log stream/ do
  ssh_cmd = "ssh -t #{@app.uid}@#{@app.hostname} tail -f #{@app.name}/logs/\\*"

  stdout, stdin, pid = PTY.spawn ssh_cmd

  @ssh_cmd = {
    :pid => pid,
    :stdin => stdin,
    :stdout => stdout,
  }

end

Given /I wait (\d+) second(s)?$/ do |sec, ignore|
  sleep(sec.to_i)
end

When /^I request the logs via SSH$/ do
  ssh_cmd = "ssh -t #{@app.uid}@#{@app.hostname} tail -f #{@app.name}/logs/\\*"

  stdout, stdin, pid = PTY.spawn ssh_cmd

  @ssh_cmd = {
    :pid => pid,
    :stdout => stdout,
  }
end

When /^I terminate the SSH log stream$/ do
  begin
    # check if the PID still exists
    Process.kill("TERM", @ssh_cmd[:pid])
    exit_code = -1

    # Don't let a command run more than 5 minutes
    Timeout::timeout(600) do
      ignored, status = Process::waitpid2 @ssh_cmd[:pid]
      exit_code = status.exitstatus
    end
  rescue PTY::ChildExited
    # Completed as expected
  end

  outstring = @ssh_cmd[:stdout].read
  $logger.debug("Standard Output:\n#{outstring}")
end


Then /^there will be (no|\d+) tail processes running( in (\d+) seconds)?$/ do |expect, ignore, timeout|
  # convert to integer
  expect = (expect == "no" ? 0 : expect.to_i)
  timeout = timeout ? timeout.to_i : 0
  sleep timeout
  pcount = num_procs @app.uid, "tail"
  pcount.should be == expect
end
