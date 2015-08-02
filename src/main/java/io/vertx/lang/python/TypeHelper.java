package io.vertx.lang.python;

import java.util.List;
import java.util.Set;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.function.Function;
import java.lang.Number;

public class TypeHelper {

  public static <T> List<T> listToT(List<Number> listT, Function<? super Number, T> func) {
    List<T> ret = listT.stream()
                     .map(func)
                     .collect(Collectors.toList());
    return ret;
  }

  public static <T> Set<T> setToT(Set<Number> setT, Function<? super Number, T> func) {
    Set<T> ret = setT.stream()
                     .map(func)
                     .collect(Collectors.toSet());
    return ret;
  }

  public static <S, T> Map<S, T> mapToT(Map<S, Number> mapT, Function<? super Number, T> func) {
    Map<S, T> ret = mapT.entrySet()
                     .stream()
                     .collect(Collectors.toMap(Map.Entry::getKey,
                                               e-> func.apply(e.getValue())));
    return ret;
  }

  public static List<Byte> toByteList(List<Number> listByte) {
    return listToT(listByte, Number::byteValue);
  }
  public static List<Short> toShortList(List<Number> listShort) {
    return listToT(listShort, Number::shortValue);
  }

  public static Set<Byte> toByteSet(Set<Number> setByte) {
    return setToT(setByte, Number::byteValue);
  }
  public static Set<Short> toShortSet(Set<Number> setShort) {
    return setToT(setShort, Number::shortValue);
  }

  public static <T> Map<T, Byte> toByteMap(Map<T, Number> mapByte) {
    return mapToT(mapByte, Number::byteValue);
  }
  public static <T> Map<T, Short> toShortMap(Map<T, Number> mapShort) {
    return mapToT(mapShort, Number::shortValue);
  }
}
