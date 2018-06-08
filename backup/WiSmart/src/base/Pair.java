/*
Pair.java:
Version: 1.0
dependencies:
Authors: Franco Minucci
emails: {name.surname}@esat.kuleuven.be
*/
package base;

import java.util.Objects;

public class Pair<X,Y> {
    public final X first;
    public final Y second;

    public Pair(X x, Y y){
        this.first = x;
        this.second = y;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Pair<?, ?> pair = (Pair<?, ?>) o;
        return Objects.equals(first, pair.first);
    }

    @Override
    public int hashCode() {

        return Objects.hash(first);
    }

    @Override
    public String toString() {
        return "Pair{" +
                "x=" + first +
                ", y=" + second +
                '}';
    }
}
