use strict;
my $data = "3,1,4,0,2,3,5";

my $dup = finder($data);

print "dup is '$dup'\n";

sub finder {
	my @dupfinder;
	my @array = split(',',$data);

	for(my $i = 0; $i < scalar @array; $i++) {
		if($dupfinder[$array[$i]] ne "") {
			return $array[$i];
		}
		$dupfinder[$array[$i]] = $array[$i];
	}
}

=begin remarks
================================================================================
Job Description: Senior Developer

This solution is sufficient, but watching the candidate find it was troubling.
The doubly indexed arrays caused a fair amount of confusion during dev.

The misunderstanding of unset values versus empty strings (ne "") is something
to probe into as well, as that could be from a concious decision that the code
will still work based on knowedge of perl's mechanics or, as it was in this
case, a misunderstanding of datatypes vs displayed output.

Use strict is great though, and the sub is fine (though I don't like the
stringly-typed data passing.
================================================================================
=end remarks
