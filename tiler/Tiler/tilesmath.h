#ifndef TILESMATH_H
#define TILESMATH_H

#define TILE_RESOLUTION 256
// Add error handling and notification methods
#include <stdexcept>

#include <vector>
#include <stdexcept>

int powint(int v, int p) noexcept;
double Resolution(int zoom) noexcept;
std::pair<double, double> MetersToLatLon(std::pair<double, double> m) noexcept;
std::pair<double, double> LatLonToMeters(double lat, double lon) noexcept;
std::pair<double, double> PixelsToMeters(double px, double py, int zoom) noexcept;
std::pair<double, double> MetersToPixels(std::pair<double, double> mxy, double zoom) noexcept;
std::pair<double, double> tilePixelToLatLon(double x, double y, int zoom) noexcept;

#endif // TILESMATH_H
