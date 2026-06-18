use LWP::UserAgent;

my $ua = LWP::UserAgent->new;
$ua->timeout(10);

my $response = $ua->get('http://127.0.0.1:8000');

print "Status: " . $response->status_line . "\n";
print "Success: " . $response->is_success . "\n";