# EvtSrc the other only source of truth (next to 42)

The motivation for this little project is to experiment with an event
sourced software architecture solving the inconsistency problem of
horizontal scaling as well as the dependency problem.  An example for
the former problem would be to have two services s1 and s2 of the same
type which get an identical request r(s1), r(s2), i.e. create a new user
named "Jacky".  Additionally we have the constrain that a user name must
be unique.  Assuming there is no user "Jacky" yet, both requests are
valid but only until one of them goes through.  The later problem
appears if r(s1) depends on an (successful) operation o(s2).  Commonly
the later problem is solved through intercommunication of components,
i.e. s1 talks to s2.  But allowing intercommunication of components
leads to an exponential growth of communications paths in dependency of
the number of components.  This makes it hard to reason about the whole
system as it grows.  Therefor I want to experiment here with an approach
where components only communicate with the event source and not with
each other.  Of course for an realistic example we also need to somehow
expose the features of our system hence we would have a second
communication hot spot.  Anyway with the here used approach the growth
of communication paths is constant.

The second reason for this little project is to practice python.