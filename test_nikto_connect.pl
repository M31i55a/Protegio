use IO::Socket::INET;

print "Test connexion 127.0.0.1:8000...\n";
my $sock = IO::Socket::INET->new(
    PeerAddr => '127.0.0.1',
    PeerPort => 8000,
    Proto    => 'tcp',
    Timeout  => 10,
);

if ($sock) {
    print "Connexion reussie sur 127.0.0.1:8000!\n";
    $sock->close();
} else {
    print "ECHEC 127.0.0.1: $!\n";
}

print "Test connexion localhost:8000...\n";
my $sock2 = IO::Socket::INET->new(
    PeerAddr => 'localhost',
    PeerPort => 8000,
    Proto    => 'tcp',
    Timeout  => 10,
);

if ($sock2) {
    print "Connexion reussie sur localhost:8000!\n";
    $sock2->close();
} else {
    print "ECHEC localhost: $!\n";
}