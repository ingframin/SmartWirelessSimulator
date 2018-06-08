package base;

import java.util.List;
/**
 * This is the base interface to define a strategy to select an AP Node.
 * For more info, see: <a href="https://en.wikipedia.org/wiki/Strategy_pattern">Strategy Pattern</a>
 * @author fminucci
 *
 */
public interface SelectStrategy {

	/**
	 * This method performs the selection of an access point node depending on the chosen strategy.
	 * @param nodes the list of nodes among which perform the selection
	 * @return AccessPointNode - the selected AP Node
	 */
    public AccessPointNode selectAP(List<Node> nodes);

}
