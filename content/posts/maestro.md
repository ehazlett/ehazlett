Date: 2012-04-07
Title: Maestro: DevOps Management
tags: [sysadmin, devops]

## Enter the Maestro

In the sysadmin world there are many tools that make the job easier.  Infrastructure management tools like [Puppet](http://puppetlabs.com), [Chef](http://www.opscode.com/chef/), and [Fabric](http://fabfile.org) (just to name a few) make tasks such as setting up and configuring machines much simpler than before.  I am a huge fan of Puppet and have been using it for almost a year now.  However, there are things that tools such as Puppet or Chef seem like overkill to me.  For instance, running a one-off command across a number of instances - where a Puppet manifest or Chef recipe might be overkill, Fabric excels in this area.  However, if you are running in a dynamic environment such as Amazon or Rackspace where hostnames/IPs change, maintaining a list of hosts or roledefs in Fabric can get cumbersome.

On another note, application deployments are just as tedious.  In my day job, I previously used Puppet for deployments.  It was a still a multi-step dance, but Puppet made things such as making sure the app servers were up to date and at the same system level config much easier. However, there was still manual intervention during deployment for things like taking certain instances out of the load balancer pool, etc.  Introduce new languages and frameworks and this gets more tedious.  Puppet and Chef are great for repetitive tasks, but if you need to adjust something mid-stream, you have to manually intervene.

With all of this in mind, I created [Maestro](https://github.com/ehazlett/maestro).  It's not meant to be a complete, one-stop solution for all of the above, but rather to help.  Maestro uses Fabric and [Apache Libcloud](http://libcloud.apache.org/) under the covers for SSH and cloud integration.  Besides the normal, great features Fabric comes with out of the box, Maestro can integrate with cloud providers for running tasks.  For instance, running a command across all EC2 instances in a region is as simple as `fab nodes:ec2 sys.run_command:"command"`.  Similarly, running that same command across Rackspace instances is `fab nodes:rackspace sys.run_command:"command"`.  You can also filter instances for tasks like `fab nodes:ec2,^appserver sys.run_command:"command"`.  The next feature will be application deployments.

Help is welcome, so fork away!

