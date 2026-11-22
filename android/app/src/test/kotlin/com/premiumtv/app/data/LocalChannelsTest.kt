package com.premiumtv.app.data

import android.app.Application
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config

/**
 * Local-channel area detection (1.1.19).
 *
 * 1.1.18 taught the apps that "nearest" is not "yours": a fix in Wilkes-Barre
 * was being saved as Philadelphia. 1.1.19 finishes the idea. A fix inside a
 * published cluster - Dallas, Fort Worth and Garland are separate entries a
 * short drive apart - is inside several markets at once, so the directory
 * reports every market within the radius, nearest first, and the dialog offers
 * the rest as alternatives. The city field stops depending on the typist.
 */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [28], application = Application::class)
class LocalChannelsTest {

    private fun directory(): LocalDirectory = LocalChannels.parse(
        """
        {
          "schema": 2,
          "countries": [{ "code": "US", "name": "United States" }],
          "states": [
            { "code": "PA", "name": "Pennsylvania" },
            { "code": "TX", "name": "Texas" },
            { "code": "MN", "name": "Minnesota" }
          ],
          "zip_ranges": [["150", "196", "PA"]],
          "zip_prefixes": [
            { "prefix": "176", "state": "PA", "market": "USLNS",
              "latitude": 40.04, "longitude": -76.31 }
          ],
          "markets": [
            {
              "id": "USLNS", "city": "Lancaster", "state": "PA",
              "state_name": "Pennsylvania", "latitude": 40.0407, "longitude": -76.3091,
              "stations": [
                { "callsign": "WGAL", "network": "NBC", "name": "WGAL 8",
                  "city": "Lancaster", "channel_id": "NBC.us@WGAL",
                  "url": "https://example.test/wgal", "backup_urls": [] }
              ]
            },
            {
              "id": "USDFW", "city": "Dallas", "state": "TX",
              "state_name": "Texas", "latitude": 32.7767, "longitude": -96.7970,
              "stations": [
                { "callsign": "WFAA", "network": "", "name": "WFAA 8",
                  "city": "Dallas", "channel_id": "", "url": "https://example.test/wfaa",
                  "backup_urls": [] }
              ]
            },
            {
              "id": "USFTW", "city": "Fort Worth", "state": "TX",
              "state_name": "Texas", "latitude": 32.7555, "longitude": -97.3308,
              "stations": [
                { "callsign": "WBAP", "network": "", "name": "WBAP",
                  "city": "Fort Worth", "channel_id": "", "url": "https://example.test/wbap",
                  "backup_urls": [] }
              ]
            },
            {
              "id": "USGST", "city": "Saint Paul", "state": "MN",
              "state_name": "Minnesota", "latitude": 44.9537, "longitude": -93.0900,
              "stations": [
                { "callsign": "KSTP", "network": "", "name": "KSTP 5",
                  "city": "Saint Paul", "channel_id": "", "url": "https://example.test/kstp",
                  "backup_urls": [] }
              ]
            }
          ]
        }
        """.trimIndent(),
    )

    @Test
    fun aFixFindsTheMarketItIsIn() {
        val local = directory()
        val area = local.nearbyMarketsWithDistance(40.04, -76.30)
        assertEquals(listOf("USLNS"), area.map { it.first.id })
        assertTrue("the fix is inside Lancaster", area.first().second < 5.0)
        assertEquals("PA", local.stateForLocation(40.04, -76.30))
    }

    @Test
    fun aFixInsideAClusterReportsEveryMarketInRangeNearestFirst() {
        val local = directory()
        // Dallas and Fort Worth are published as separate markets ~48 km apart,
        // so a fix in Fort Worth is inside both at once.
        val area = local.nearbyMarketsWithDistance(32.7555, -97.3308)
        assertEquals(listOf("USFTW", "USDFW"), area.map { it.first.id })
        assertTrue(area[0].second < area[1].second)
        assertTrue("Dallas is in reach", marketIsNear(area[1].second))
    }

    @Test
    fun nothingPublishedNearAFixIsEmptyNotTheNearestThing() {
        val local = directory()
        // The Atlantic: no market within the radius, so the caller says so
        // instead of naming the closest one 1,000 km away.
        assertTrue(local.nearbyMarketsWithDistance(0.0, 0.0).isEmpty())
        val unbounded = local.nearbyMarketsWithDistance(0.0, 0.0, maxKm = 20_000.0)
        assertTrue(unbounded.isNotEmpty())
        assertTrue(unbounded.first().second <= unbounded.last().second)
    }

    @Test
    fun aFixCanBeRestrictedToAState() {
        val local = directory()
        val area = local.nearbyMarketsWithDistance(40.04, -76.30, state = "PA")
        assertEquals(listOf("USLNS"), area.map { it.first.id })
        assertTrue(local.nearbyMarketsWithDistance(40.04, -76.30, state = "TX").isEmpty())
    }

    @Test
    fun aTypedCityMatchesThePlaceNotTheSpelling() {
        val local = directory()
        val normalized = local.marketsFor(LocalSelection(state = "MN", city = "St. Paul"))
        assertEquals(listOf("USGST"), normalized.map { it.id })
        assertEquals(
            listOf("USGST"),
            local.marketsFor(LocalSelection(state = "MN", city = "saint paul")).map { it.id },
        )
        // A place PremiumTV does not publish stays empty, however it is spelled.
        assertTrue(local.marketsFor(LocalSelection(city = "Wilkes Barre")).isEmpty())
        assertTrue(local.marketsFor(LocalSelection(city = "Wilkes-Barre")).isEmpty())
    }

    @Test
    fun placeNamesFoldAccentsAndPunctuation() {
        assertEquals(normalizePlace("Wilkes-Barre"), normalizePlace("Wilkes Barre"))
        assertEquals(normalizePlace("Saint Paul"), normalizePlace("St. Paul"))
        assertEquals("fort worth", normalizePlace("  Fort   Worth  "))
        assertEquals("munchen", normalizePlace("München"))
        assertEquals("", normalizePlace("   "))
    }

    @Test
    fun theRadiusBoundaryIsInclusive() {
        assertTrue(marketIsNear(0.0))
        assertTrue(marketIsNear(LOCAL_MARKET_NEAR_KM))
        assertTrue(!marketIsNear(LOCAL_MARKET_NEAR_KM + 0.1))
        assertTrue(!marketIsNear(Double.NaN))
    }

    @Test
    fun aZipStillResolvesToItsMarket() {
        val local = directory()
        assertEquals("USLNS", local.marketForZip("17603")?.id)
        assertNull(local.marketForZip("00000"))
        assertEquals("PA", local.stateForZip("17603"))
    }
}
